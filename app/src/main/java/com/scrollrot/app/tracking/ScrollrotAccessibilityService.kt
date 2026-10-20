package com.scrollrot.app.tracking

import android.accessibilityservice.AccessibilityService
import android.os.Build
import android.os.SystemClock
import android.view.accessibility.AccessibilityEvent
import com.scrollrot.app.store.TrackingStore

/**
 * Prototype: best-effort counting of vertical scroll events while a short-feed UI is
 * heuristically visible. One event is NOT guaranteed to equal one real reel.
 * Never save, upload, or log watched videos, text, captions, or messages.
 */
class ScrollrotAccessibilityService : AccessibilityService() {
    private lateinit var store: TrackingStore
    private val lastAccepted = mutableMapOf<String, Long>()
    private val lastInspected = mutableMapOf<String, Long>()
    private val feedVisible = mutableMapOf<String, Boolean>()

    override fun onServiceConnected() {
        super.onServiceConnected()
        store = TrackingStore(applicationContext)
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null || !::store.isInitialized || !store.consented()) return
        val pkg = event.packageName?.toString() ?: return
        val platform = ShortFormHeuristic.platform(pkg) ?: return
        val now = SystemClock.elapsedRealtime()
        val type = event.eventType

        if (type == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED ||
            (type == AccessibilityEvent.TYPE_VIEW_SCROLLED &&
             now - (lastInspected[pkg] ?: 0L) > 700L)) {
            // The active root might have changed since event dispatch; verify owner.
            val root = rootInActiveWindow
            feedVisible[pkg] = root?.packageName?.toString() == pkg &&
                ShortFormHeuristic.likelyShortFeed(root, platform)
            lastInspected[pkg] = now
        }
        if (type != AccessibilityEvent.TYPE_VIEW_SCROLLED || feedVisible[pkg] != true) return
        if (now - (lastAccepted[pkg] ?: 0L) < 1100L) return

        if (Build.VERSION.SDK_INT >= 28 && event.scrollDeltaY <= 0) return
        // On API 26-27 direction cannot be checked with scrollDeltaY; lower confidence.
        lastAccepted[pkg] = now
        store.add(platform)
    }

    override fun onInterrupt() { /* no-op; Android controls service lifecycle */ }
}
