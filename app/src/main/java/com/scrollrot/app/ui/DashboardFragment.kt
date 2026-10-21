package com.scrollrot.app.ui

import android.accessibilityservice.AccessibilityServiceInfo
import android.animation.ObjectAnimator
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.res.ColorStateList
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.accessibility.AccessibilityManager
import android.widget.Button
import android.widget.ProgressBar
import android.widget.Switch
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.scrollrot.app.R
import com.scrollrot.app.store.TrackingStore
import com.scrollrot.app.tracking.FloatingHudManager

/**
 * The "You" dashboard fragment matching BrainPal Image 5.
 * Features centered interactive mascot, live count, platform pills,
 * and floating HUD controls.
 */
class DashboardFragment : Fragment() {

    private lateinit var store: TrackingStore
    private var previewHudManager: FloatingHudManager? = null

    private lateinit var mascot: RotCharacterView
    private lateinit var countText: TextView
    private lateinit var moodText: TextView
    private lateinit var countIg: TextView
    private lateinit var countYt: TextView
    private lateinit var wrapSummaryText: TextView
    private lateinit var switchFloatingHud: Switch
    private lateinit var btnTestHud: Button
    private lateinit var limitText: TextView
    private lateinit var bufferText: TextView
    private lateinit var limitBar: ProgressBar
    private lateinit var permissionStatus: TextView
    private lateinit var permissionButton: Button
    private lateinit var demoButton: Button

    private var previousCount = -1
    private val mainHandler = Handler(Looper.getMainLooper())

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_you, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val context = requireContext()
        store = TrackingStore(context.applicationContext)

        initViews(view)
        setupListeners()
        refresh()

        store.addChangeListener {
            if (isAdded) refresh()
        }
    }

    private fun initViews(v: View) {
        mascot = v.findViewById(R.id.mascotView)
        countText = v.findViewById(R.id.countText)
        moodText = v.findViewById(R.id.moodText)
        countIg = v.findViewById(R.id.countIg)
        countYt = v.findViewById(R.id.countYt)
        wrapSummaryText = v.findViewById(R.id.wrapSummaryText)
        switchFloatingHud = v.findViewById(R.id.switchFloatingHud)
        btnTestHud = v.findViewById(R.id.btnTestHud)
        limitText = v.findViewById(R.id.limitText)
        bufferText = v.findViewById(R.id.bufferText)
        limitBar = v.findViewById(R.id.limitBar)
        permissionStatus = v.findViewById(R.id.permissionStatus)
        permissionButton = v.findViewById(R.id.permissionButton)
        demoButton = v.findViewById(R.id.demoButton)

        switchFloatingHud.isChecked = store.isFloatingHudEnabled()

        v.findViewById<View>(R.id.btnHelp)?.setOnClickListener {
            showDisclosure()
        }

        v.findViewById<View>(R.id.btnShare)?.setOnClickListener {
            val sendIntent = Intent().apply {
                action = Intent.ACTION_SEND
                putExtra(Intent.EXTRA_TEXT, "I have only scrolled ${store.total()} reels today using Scrollrot! Track your digital wellbeing.")
                type = "text/plain"
            }
            startActivity(Intent.createChooser(sendIntent, "Share your reels score"))
        }
    }

    private fun setupListeners() {
        switchFloatingHud.setOnCheckedChangeListener { _, isChecked ->
            store.setFloatingHudEnabled(isChecked)
        }

        btnTestHud.setOnClickListener {
            testFloatingHudOnScreen()
        }

        permissionButton.setOnClickListener {
            showDisclosure()
        }

        demoButton.setOnClickListener {
            store.add("instagram")
            refresh()
        }
    }

    private fun testFloatingHudOnScreen() {
        val context = requireContext()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(context)) {
            AlertDialog.Builder(context)
                .setTitle("Overlay Permission Needed")
                .setMessage("To preview the floating HUD widget from the app, please enable 'Display over other apps'. (Inside Instagram and YouTube Shorts, Accessibility Service displays it automatically).")
                .setPositiveButton("Open Settings") { _, _ ->
                    startActivity(Intent(
                        Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:${context.packageName}")
                    ))
                }
                .setNegativeButton("Cancel", null)
                .show()
            return
        }

        previewHudManager?.destroy()
        previewHudManager = FloatingHudManager(context, store).apply {
            resetDismissed()
            showOrUpdate("instagram")
        }

        mainHandler.postDelayed({
            previewHudManager?.hide()
        }, 6000L)
    }

    fun refresh() {
        if (!isAdded) return
        val total = store.total()
        val goal = store.dailyGoal()
        val ig = store.count("instagram")
        val yt = store.count("youtube")

        countText.text = total.toString()
        mascot.setCount(total)

        countIg.text = ig.toString()
        countYt.text = yt.toString()

        val remaining = (goal - total).coerceAtLeast(0)
        limitText.text = "Target: $total / $goal reels today"
        bufferText.text = "$remaining left >"
        limitBar.max = goal
        limitBar.progress = total.coerceAtMost(goal)

        wrapSummaryText.text = "$total reels today. See your mindful habits."

        // Mood text & progress color
        val context = requireContext()
        when {
            total < goal * 0.35 -> {
                moodText.text = "Optimal Focus ✨ · Under daily target"
                moodText.setTextColor(ContextCompat.getColor(context, R.color.accent))
                limitBar.progressTintList = ColorStateList.valueOf(ContextCompat.getColor(context, R.color.accent))
            }
            total < goal * 0.75 -> {
                moodText.text = "Mindful Browsing 🌀 · Steady pace"
                moodText.setTextColor(ContextCompat.getColor(context, R.color.cyan))
                limitBar.progressTintList = ColorStateList.valueOf(ContextCompat.getColor(context, R.color.cyan))
            }
            total < goal -> {
                moodText.text = "Fatigue Approaching ⚠️ · Take a break"
                moodText.setTextColor(ContextCompat.getColor(context, R.color.amber))
                limitBar.progressTintList = ColorStateList.valueOf(ContextCompat.getColor(context, R.color.amber))
            }
            else -> {
                moodText.text = "Brain Rot Alarm 🚨 · Daily limit exceeded"
                moodText.setTextColor(ContextCompat.getColor(context, R.color.danger))
                limitBar.progressTintList = ColorStateList.valueOf(ContextCompat.getColor(context, R.color.danger))
            }
        }

        // Tracking shield state
        val serviceActive = isServiceEnabled()
        if (serviceActive) {
            permissionStatus.text = "🟢 Tracking Shield Active · Detecting Reels & Shorts"
            permissionStatus.setTextColor(ContextCompat.getColor(context, R.color.accent))
            permissionButton.text = "Tracking Shield Enabled"
        } else {
            permissionStatus.text = "⚠️ Tracking permission not enabled · Enable to detect reels"
            permissionStatus.setTextColor(ContextCompat.getColor(context, R.color.amber))
            permissionButton.text = "Enable Reel Tracking Shield"
        }

        if (previousCount >= 0 && total != previousCount) {
            ObjectAnimator.ofFloat(countText, "scaleX", 1.0f, 1.15f, 1.0f).apply { duration = 240 }.start()
            ObjectAnimator.ofFloat(countText, "scaleY", 1.0f, 1.15f, 1.0f).apply { duration = 240 }.start()
            ObjectAnimator.ofFloat(mascot, "scaleX", 1.0f, 1.06f, 1.0f).apply { duration = 300 }.start()
        }
        previousCount = total
    }

    private fun isServiceEnabled(): Boolean {
        val am = requireContext().getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
        return am.getEnabledAccessibilityServiceList(AccessibilityServiceInfo.FEEDBACK_ALL_MASK)
            .any {
                it.resolveInfo.serviceInfo.packageName == requireContext().packageName &&
                        it.resolveInfo.serviceInfo.name.endsWith("ScrollrotAccessibilityService")
            }
    }

    private fun showDisclosure() {
        AlertDialog.Builder(requireContext())
            .setTitle("Enable Reel Tracking Shield")
            .setMessage("Scrollrot uses Android Accessibility to detect vertical swipe transitions on Instagram Reels, YouTube Shorts, Facebook Reels, and Snapchat Spotlight.\n\n" +
                    "• 100% Private: We NEVER collect, record, or transmit captions, messages, search history, or video content.\n" +
                    "• Floating HUD: Displays a live counter on top of reels so you stay mindful of your screen time.\n" +
                    "• Local First: All counts stay on your device.\n" +
                    "• Full Control: You can disable tracking anytime in Settings.")
            .setNegativeButton("Not Now", null)
            .setPositiveButton("I Agree · Open Settings") { _, _ ->
                store.saveConsent()
                startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            }.show()
    }

    override fun onDestroyView() {
        previewHudManager?.destroy()
        super.onDestroyView()
    }
}
