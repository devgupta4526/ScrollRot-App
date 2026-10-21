package com.scrollrot.app.tracking

import android.accessibilityservice.AccessibilityService
import android.content.Context
import android.os.Build
import android.os.SystemClock
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.view.accessibility.AccessibilityEvent
import com.scrollrot.app.store.TrackingStore

/**
 * Core Accessibility Service for detecting vertical short-form reel swipes
 * across Instagram Reels, YouTube Shorts, Facebook Reels, and Snapchat Spotlight.
 *
 * Automatically displays and updates the in-reel floating HUD widget overlay,
 * debounces reel transitions, and respects user consent and pause toggles.
 * Never collects captions, messages, view hierarchy, or private media.
 */
class ScrollrotAccessibilityService : AccessibilityService() {

    private lateinit var store: TrackingStore
    private var hudManager: FloatingHudManager? = null
    private val lastAccepted = mutableMapOf<String, Long>()
    private val lastInspected = mutableMapOf<String, Long>()
    private val isShortFeedActive = mutableMapOf<String, Boolean>()
    private var vibrator: Vibrator? = null

    override fun onServiceConnected() {
        super.onServiceConnected()
        store = TrackingStore(applicationContext)
        hudManager = FloatingHudManager(this, store)

        vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
            vm?.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
        }
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null || !::store.isInitialized || !store.consented()) return

        val pkg = event.packageName?.toString() ?: return
        val platform = ShortFormHeuristic.platform(pkg)

        if (platform == null) {
            // User is in an unsupported app or home screen: hide floating widget
            hudManager?.hide()
            return
        }

        val now = SystemClock.elapsedRealtime()
        val type = event.eventType

        // 1. Periodically verify whether active screen is a short-video feed
        if (type == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED ||
            type == AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED ||
            now - (lastInspected[pkg] ?: 0L) > 600L
        ) {
            val root = rootInActiveWindow
            val active = root != null && root.packageName?.toString() == pkg &&
                    ShortFormHeuristic.likelyShortFeed(root, platform)
            isShortFeedActive[pkg] = active
            lastInspected[pkg] = now

            if (active) {
                hudManager?.showOrUpdate(platform)
            } else {
                hudManager?.hide()
            }
        }

        val inFeed = isShortFeedActive[pkg] == true
        if (!inFeed) return

        // 2. Detect candidate reel swipes / page selections
        val isScrollOrPageSelect = type == AccessibilityEvent.TYPE_VIEW_SCROLLED ||
                type == AccessibilityEvent.TYPE_VIEW_SELECTED

        if (isScrollOrPageSelect) {
            // Debounce: ensure at least 850ms between reel transitions
            val timeSinceLast = now - (lastAccepted[pkg] ?: 0L)
            if (timeSinceLast >= 850L) {
                lastAccepted[pkg] = now
                store.add(platform)

                // Update the floating widget
                hudManager?.showOrUpdate(platform)

                // Subtle haptic pulse
                triggerHapticFeedback()
            }
        }
    }

    private fun triggerHapticFeedback() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vibrator?.vibrate(VibrationEffect.createOneShot(18, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                vibrator?.vibrate(18)
            }
        } catch (_: Exception) {}
    }

    override fun onInterrupt() {
        hudManager?.hide()
    }

    override fun onDestroy() {
        hudManager?.destroy()
        hudManager = null
        super.onDestroy()
    }
}
