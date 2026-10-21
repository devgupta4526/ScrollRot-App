package com.scrollrot.app.tracking

import android.accessibilityservice.AccessibilityService
import android.animation.ObjectAnimator
import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.ProgressBar
import android.widget.TextView
import com.scrollrot.app.R
import com.scrollrot.app.store.TrackingStore
import kotlin.math.abs

/**
 * Manages the floating in-reel HUD widget overlay that floats on top of
 * Instagram Reels, YouTube Shorts, etc.
 *
 * Provides live reel count, mascot emotion indicator, drag-to-reposition,
 * and expandable breakdown panel.
 */
class FloatingHudManager(
    private val context: Context,
    private val store: TrackingStore
) {
    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val mainHandler = Handler(Looper.getMainLooper())
    private var hudView: View? = null
    private var isAttached = false
    private var isExpanded = false
    private var isUserDismissed = false
    private var params: WindowManager.LayoutParams? = null

    private val collapseRunnable = Runnable {
        if (isExpanded) {
            isExpanded = false
            hudView?.findViewById<View>(R.id.hudExpandedPanel)?.visibility = View.GONE
        }
    }

    fun showOrUpdate(currentPlatform: String? = null) {
        if (!store.isFloatingHudEnabled() || isUserDismissed) return

        mainHandler.post {
            try {
                if (hudView == null) {
                    createHudView()
                }

                updateContent(currentPlatform)

                if (!isAttached && hudView != null && params != null) {
                    windowManager.addView(hudView, params)
                    isAttached = true
                }
            } catch (e: Exception) {
                // Silently handle window token errors on unexpected app transitions
            }
        }
    }

    fun hide() {
        mainHandler.post {
            try {
                if (isAttached && hudView != null) {
                    windowManager.removeView(hudView)
                    isAttached = false
                }
            } catch (e: Exception) {
                // View might already be detached
            }
        }
    }

    fun resetDismissed() {
        isUserDismissed = false
    }

    private fun createHudView() {
        val inflater = LayoutInflater.from(context)
        val view = inflater.inflate(R.layout.layout_floating_hud, null)

        val windowType = when {
            context is AccessibilityService -> WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.O -> WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else -> @Suppress("DEPRECATION") WindowManager.LayoutParams.TYPE_PHONE
        }

        val lp = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            windowType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 32
            y = 380
        }

        setupTouchListener(view, lp)

        view.findViewById<View>(R.id.hudDismissText).setOnClickListener {
            isUserDismissed = true
            hide()
        }

        hudView = view
        params = lp
    }

    private fun setupTouchListener(view: View, lp: WindowManager.LayoutParams) {
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f

        view.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = lp.x
                    initialY = lp.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    val deltaX = (event.rawX - initialTouchX).toInt()
                    val deltaY = (event.rawY - initialTouchY).toInt()
                    lp.x = initialX + deltaX
                    lp.y = initialY + deltaY
                    if (isAttached) {
                        try {
                            windowManager.updateViewLayout(view, lp)
                        } catch (_: Exception) {}
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    val distMoved = abs(event.rawX - initialTouchX) + abs(event.rawY - initialTouchY)
                    if (distMoved < 15) {
                        // Click gesture: toggle expand/collapse
                        toggleExpand()
                    }
                    true
                }
                else -> false
            }
        }
    }

    private fun toggleExpand() {
        isExpanded = !isExpanded
        hudView?.findViewById<View>(R.id.hudExpandedPanel)?.visibility =
            if (isExpanded) View.VISIBLE else View.GONE

        mainHandler.removeCallbacks(collapseRunnable)
        if (isExpanded) {
            mainHandler.postDelayed(collapseRunnable, 4500L)
        }
    }

    private fun updateContent(currentPlatform: String?) {
        val view = hudView ?: return
        val total = store.total()
        val goal = store.dailyGoal()

        val countText = view.findViewById<TextView>(R.id.hudCount)
        val emojiText = view.findViewById<TextView>(R.id.hudEmoji)
        val targetText = view.findViewById<TextView>(R.id.hudTargetText)
        val platformText = view.findViewById<TextView>(R.id.hudPlatformText)
        val progressBar = view.findViewById<ProgressBar>(R.id.hudProgressBar)
        val root = view.findViewById<View>(R.id.hudRoot)

        countText.text = total.toString()

        val headContainer = view.findViewById<View>(R.id.hudHeadContainer)

        // Mascot status emoji & background styling matching BrainPal in-reel overlay
        when {
            total < goal * 0.4 -> {
                emojiText.text = "✨"
                countText.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#16A34A"))
            }
            total < goal * 0.75 -> {
                emojiText.text = "🌀"
                countText.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#D97706"))
            }
            total < goal -> {
                emojiText.text = "🧠"
                countText.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#EA580C"))
            }
            else -> {
                emojiText.text = "💀"
                countText.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#DC2626"))
            }
        }

        targetText.text = "$total / $goal daily limit (${(goal - total).coerceAtLeast(0)} left)"
        platformText.text = "IG: ${store.count("instagram")} · YT: ${store.count("youtube")} · FB: ${store.count("facebook")}"
        progressBar.max = goal
        progressBar.progress = total.coerceAtMost(goal)

        // Pop animation on count change
        ObjectAnimator.ofFloat(countText, "scaleX", 1.0f, 1.25f, 1.0f).apply { duration = 240 }.start()
        ObjectAnimator.ofFloat(countText, "scaleY", 1.0f, 1.25f, 1.0f).apply { duration = 240 }.start()
    }

    fun destroy() {
        hide()
        hudView = null
        params = null
    }
}
