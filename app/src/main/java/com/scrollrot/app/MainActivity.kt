package com.scrollrot.app

import android.accessibilityservice.AccessibilityServiceInfo
import android.animation.ObjectAnimator
import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.view.accessibility.AccessibilityManager
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import android.app.Activity
import com.scrollrot.app.store.TrackingStore
import com.scrollrot.app.ui.RotCharacterView

class MainActivity : Activity() {
    private lateinit var store: TrackingStore
    private lateinit var countText: TextView
    private lateinit var mascot: RotCharacterView
    private lateinit var moodText: TextView
    private lateinit var limitText: TextView
    private lateinit var limitBar: ProgressBar
    private lateinit var appsText: TextView
    private lateinit var permissionStatus: TextView
    private var previousCount = -1
    private var demoCount: Int? = null
    private val ticker = android.os.Handler(android.os.Looper.getMainLooper())
    private val update = object : Runnable {
        override fun run() { refresh(); ticker.postDelayed(this, 1000L) }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        store = TrackingStore(applicationContext)
        countText = findViewById(R.id.countText)
        mascot = findViewById(R.id.mascotView)
        moodText = findViewById(R.id.moodText)
        limitText = findViewById(R.id.limitText)
        limitBar = findViewById(R.id.limitBar)
        appsText = findViewById(R.id.appsText)
        permissionStatus = findViewById(R.id.permissionStatus)

        findViewById<Button>(R.id.permissionButton).setOnClickListener { showDisclosure() }
        findViewById<Button>(R.id.demoButton).setOnClickListener {
            demoCount = (demoCount ?: 0) + 1 // Preview is not stored as real tracking.
            refresh()
        }
        refresh()
    }

    override fun onStart() { super.onStart(); ticker.post(update) }
    override fun onStop() { ticker.removeCallbacks(update); super.onStop() }

    private fun refresh() {
        val total = demoCount ?: store.total()
        countText.text = total.toString()
        mascot.setCount(total)
        moodText.text = when {
            total < 25 -> "Looking fresh ✨"
            total < 75 -> "Getting distracted 🌀"
            total < 150 -> "Time for a break 🌙"
            else -> "Rest mode recommended 💜"
        }
        limitText.text = "$total / 100 reels"
        limitBar.progress = total.coerceAtMost(100)
        appsText.text = if (demoCount != null) "Preview mode · not saved to history" else
            "Instagram · ${store.count("instagram")}\n" +
            "YouTube · ${store.count("youtube")}\n" +
            "Facebook · ${store.count("facebook")}\n" +
            "Snapchat · ${store.count("snapchat")}" 
        findViewById<TextView>(R.id.countLabel).text = if (demoCount != null) "demo swipes (not saved)" else "reel swipes today (estimated)"
        permissionStatus.text = if (demoCount != null) "Preview mode · restart app to return to actual counts" else if (isServiceEnabled())
            "Tracking permission enabled · counts may be approximate"
        else "Tracking permission not enabled"
        if (previousCount >= 0 && total != previousCount) {
            ObjectAnimator.ofFloat(countText, "scaleX", 1.0f, 1.12f, 1.0f).apply { duration = 280 }.start()
            ObjectAnimator.ofFloat(countText, "scaleY", 1.0f, 1.12f, 1.0f).apply { duration = 280 }.start()
            ObjectAnimator.ofFloat(mascot, "scaleX", 1.0f, 1.055f, 1.0f).apply { duration = 350 }.start()
        }
        previousCount = total
    }

    private fun isServiceEnabled(): Boolean {
        val am = getSystemService(ACCESSIBILITY_SERVICE) as AccessibilityManager
        return am.getEnabledAccessibilityServiceList(AccessibilityServiceInfo.FEEDBACK_ALL_MASK)
            .any { it.resolveInfo.serviceInfo.packageName == packageName &&
                   it.resolveInfo.serviceInfo.name.endsWith("ScrollrotAccessibilityService") }
    }

    private fun showDisclosure() {
        AlertDialog.Builder(this)
            .setTitle("Enable reel counting?")
            .setMessage("Scrollrot requests Accessibility access to detect scrolling and screen changes inside Instagram, YouTube, Facebook and Snapchat. Android accessibility access can expose visible screen content. Scrollrot's prototype examines limited screen labels to estimate reel transitions; it does not save messages, captions or videos, or upload activity. Only daily counts are stored on your device. You can turn access off anytime in Android Settings. Detection is experimental and may miss or double-count reels.")
            .setNegativeButton("Not now", null)
            .setPositiveButton("I agree · Open Settings") { _, _ ->
                store.saveConsent()
                startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            }.show()
    }
}
