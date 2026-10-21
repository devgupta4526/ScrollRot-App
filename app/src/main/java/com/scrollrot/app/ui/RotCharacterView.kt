package com.scrollrot.app.ui

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import android.view.animation.AccelerateDecelerateInterpolator
import android.view.animation.OvershootInterpolator
import kotlin.math.PI
import kotlin.math.sin

/**
 * Premium, interactive, Canvas-rendered animated mascot for Scrollrot.
 * Features breathing, eye blinking, aura glow, phase transitions based on
 * reel count, and touch-reactive spring bounce animations.
 */
class RotCharacterView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : View(context, attrs) {

    private val p = Paint(Paint.ANTI_ALIAS_FLAG)
    private val path = Path()
    private var phase = 0f
    private var blinkPhase = 0f
    private var tapScale = 1.0f
    private var count = 0
    private var breatheAnim: ValueAnimator? = null
    private var blinkAnim: ValueAnimator? = null
    private var tapAnim: ValueAnimator? = null

    private val ink = Color.rgb(9, 13, 22)
    private val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        val vm = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
        vm?.defaultVibrator
    } else {
        @Suppress("DEPRECATION")
        context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
    }

    init {
        isClickable = true
    }

    fun setCount(value: Int) {
        count = value
        invalidate()
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (event.action == MotionEvent.ACTION_DOWN) {
            triggerBounce()
            performClick()
            return true
        }
        return super.onTouchEvent(event)
    }

    override fun performClick(): Boolean {
        super.performClick()
        return true
    }

    private fun triggerBounce() {
        tapAnim?.cancel()
        tapAnim = ValueAnimator.ofFloat(0.85f, 1.15f, 1.0f).apply {
            duration = 450
            interpolator = OvershootInterpolator(2.5f)
            addUpdateListener {
                tapScale = it.animatedValue as Float
                invalidate()
            }
            start()
        }

        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vibrator?.vibrate(VibrationEffect.createOneShot(24, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                vibrator?.vibrate(24)
            }
        } catch (_: Exception) {}
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        startAnimations()
    }

    override fun onDetachedFromWindow() {
        stopAnimations()
        super.onDetachedFromWindow()
    }

    private fun startAnimations() {
        if (!ValueAnimator.areAnimatorsEnabled()) return

        // 1. Continuous breathing and aura pulse
        breatheAnim = ValueAnimator.ofFloat(0f, 1f).apply {
            duration = 2400
            repeatCount = ValueAnimator.INFINITE
            interpolator = AccelerateDecelerateInterpolator()
            addUpdateListener {
                phase = it.animatedValue as Float
                invalidate()
            }
            start()
        }

        // 2. Periodic natural eye blink
        blinkAnim = ValueAnimator.ofFloat(0f, 1f).apply {
            duration = 3200
            repeatCount = ValueAnimator.INFINITE
            addUpdateListener {
                val v = it.animatedValue as Float
                // Blink happens quickly between 0.88 and 0.98 of the cycle
                blinkPhase = if (v > 0.88f && v < 0.98f) {
                    val progress = (v - 0.88f) / 0.10f
                    sin(progress * PI).toFloat()
                } else 0f
                invalidate()
            }
            start()
        }
    }

    private fun stopAnimations() {
        breatheAnim?.cancel()
        breatheAnim = null
        blinkAnim?.cancel()
        blinkAnim = null
        tapAnim?.cancel()
        tapAnim = null
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val w = width.toFloat()
        val h = height.toFloat()
        val s = minOf(w / 240f, h / 214f) * tapScale

        canvas.save()
        canvas.translate((w - 240f * s) / 2f, (h - 214f * s) / 2f)
        canvas.scale(s, s)

        val bob = sin(phase * 2 * PI).toFloat() * 5f
        val auraPulse = sin(phase * 2 * PI).toFloat() * 6f

        // 1. Neon Aura Glow (Mood-reactive)
        val (auraColor1, auraColor2) = when {
            count < 25 -> Pair(Color.argb(32, 179, 255, 114), Color.argb(60, 56, 189, 248))
            count < 75 -> Pair(Color.argb(32, 56, 189, 248), Color.argb(60, 139, 92, 246))
            count < 125 -> Pair(Color.argb(35, 245, 158, 11), Color.argb(65, 139, 92, 246))
            else -> Pair(Color.argb(45, 244, 63, 94), Color.argb(75, 139, 92, 246))
        }

        p.style = Paint.Style.FILL
        p.color = auraColor1
        canvas.drawCircle(120f, 100f, 96f + auraPulse, p)
        p.color = auraColor2
        canvas.drawCircle(120f, 100f, 76f + auraPulse * 0.6f, p)

        canvas.save()
        canvas.translate(0f, bob)

        // 2. Soft Shadow and Feet
        p.color = Color.argb(60, 0, 0, 0)
        canvas.drawOval(RectF(60f, 185f, 180f, 202f), p)

        p.color = ink
        canvas.drawRoundRect(RectF(76f, 156f, 102f, 190f), 10f, 10f, p)
        canvas.drawRoundRect(RectF(140f, 156f, 166f, 190f), 10f, 10f, p)

        // 3. Body Color Transformation
        val bodyColor = when {
            count < 25 -> Color.rgb(179, 255, 114)  // Neon Volt / Lime
            count < 75 -> Color.rgb(56, 189, 248)   // Electric Cyan
            count < 125 -> Color.rgb(251, 191, 36)  // Cyber Amber
            count < 175 -> Color.rgb(167, 139, 250) // Melting Lavender
            else -> Color.rgb(244, 63, 94)          // Alert Rose Red
        }

        p.color = bodyColor
        path.reset()
        // Organic, cute cloud-blob geometry
        path.moveTo(62f, 146f)
        path.cubicTo(29f, 135f, 31f, 92f, 56f, 79f)
        path.cubicTo(39f, 54f, 66f, 30f, 91f, 40f)
        path.cubicTo(103f, 18f, 140f, 18f, 151f, 40f)
        path.cubicTo(181f, 29f, 204f, 57f, 185f, 79f)
        path.cubicTo(213f, 98f, 207f, 138f, 177f, 146f)
        path.cubicTo(170f, 176f, 74f, 177f, 62f, 146f)
        path.close()
        canvas.drawPath(path, p)

        // Body Outline
        p.style = Paint.Style.STROKE
        p.strokeWidth = 5.5f
        p.color = ink
        canvas.drawPath(path, p)
        p.style = Paint.Style.FILL

        // 4. Mascot Crown / Spiral Antenna
        p.color = Color.argb(85, 9, 13, 22)
        p.style = Paint.Style.STROKE
        p.strokeWidth = 3.5f
        path.reset()
        path.moveTo(105f, 52f)
        path.cubicTo(92f, 70f, 127f, 82f, 142f, 65f)
        canvas.drawPath(path, p)
        p.style = Paint.Style.FILL

        // 5. Expressive Eyes with Natural Blinking
        p.color = ink
        val eyeHeight = (7f * (1f - blinkPhase)).coerceAtLeast(1.2f)

        if (count < 65) {
            // Happy round eyes with shine
            canvas.drawOval(RectF(84f, 111f - eyeHeight, 98f, 111f + eyeHeight), p)
            canvas.drawOval(RectF(146f, 111f - eyeHeight, 160f, 111f + eyeHeight), p)

            // Sparkle shine in eyes (when not blinking)
            if (blinkPhase < 0.3f) {
                p.color = Color.WHITE
                canvas.drawCircle(88f, 108f, 2.2f, p)
                canvas.drawCircle(150f, 108f, 2.2f, p)
                p.color = ink
            }
        } else if (count < 125) {
            // Distracted / Spiral eye expression
            p.style = Paint.Style.STROKE
            p.strokeWidth = 3.2f
            canvas.drawCircle(91f, 111f, 7f, p)
            canvas.drawCircle(153f, 111f, 7f, p)
            p.style = Paint.Style.FILL
            canvas.drawCircle(91f, 111f, 3f, p)
            canvas.drawCircle(153f, 111f, 3f, p)

            // Sweat drop on forehead
            p.color = Color.rgb(56, 189, 248)
            canvas.drawCircle(172f, 72f, 4.5f, p)
            p.color = ink
        } else {
            // Rotting / Critical fatigue eyes
            p.style = Paint.Style.STROKE
            p.strokeWidth = 4f
            // Angled drowsy eyelids
            canvas.drawLine(83f, 107f, 99f, 115f, p)
            canvas.drawLine(161f, 107f, 145f, 115f, p)
            p.style = Paint.Style.FILL
            canvas.drawCircle(91f, 115f, 4f, p)
            canvas.drawCircle(153f, 115f, 4f, p)
        }

        // 6. Mouth Expressions
        p.style = Paint.Style.STROKE
        p.strokeWidth = 4f
        p.strokeCap = Paint.Cap.ROUND
        path.reset()

        when {
            count < 65 -> {
                // Wide cheerful smile
                path.moveTo(102f, 129f)
                path.quadTo(122f, 147f, 142f, 129f)
            }
            count < 125 -> {
                // Wavy confused mouth
                path.moveTo(104f, 134f)
                path.quadTo(114f, 128f, 124f, 134f)
                path.quadTo(134f, 140f, 142f, 134f)
            }
            else -> {
                // Frowning exhausted mouth
                path.moveTo(104f, 140f)
                path.quadTo(122f, 126f, 142f, 140f)
            }
        }
        canvas.drawPath(path, p)
        p.style = Paint.Style.FILL

        // 7. Melting Sludge & Alarm Marks
        if (count >= 100) {
            p.color = ink
            p.strokeWidth = 3.2f
            p.style = Paint.Style.STROKE
            path.reset()
            path.moveTo(151f, 41f)
            path.lineTo(140f, 62f)
            path.lineTo(153f, 76f)
            path.lineTo(142f, 94f)
            canvas.drawPath(path, p)
            p.style = Paint.Style.FILL
        }

        if (count >= 150) {
            // Alarm crack / sweat marks
            p.color = Color.argb(190, 244, 63, 94)
            p.strokeWidth = 3.5f
            p.style = Paint.Style.STROKE
            canvas.drawLine(58f, 112f, 84f, 144f, p)
            canvas.drawLine(186f, 112f, 160f, 144f, p)
            p.style = Paint.Style.FILL
        }

        canvas.restore() // Undo bob

        // 8. Floating Sparkles
        p.color = when {
            count < 65 -> Color.rgb(179, 255, 114)
            count < 125 -> Color.rgb(245, 158, 11)
            else -> Color.rgb(244, 63, 94)
        }
        canvas.drawCircle(34f, 52f, 4f, p)
        canvas.drawCircle(212f, 128f, 4.5f, p)
        canvas.drawCircle(48f, 168f, 3f, p)

        canvas.restore() // Undo scale/translate
    }
}
