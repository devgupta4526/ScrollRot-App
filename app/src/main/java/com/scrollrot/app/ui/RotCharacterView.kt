package com.scrollrot.app.ui

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View
import android.view.animation.AccelerateDecelerateInterpolator
import kotlin.math.PI
import kotlin.math.sin

/** Original Scrollrot blob mascot rendered on Canvas. No copyrighted character assets. */
class RotCharacterView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : View(context, attrs) {
    private val p = Paint(Paint.ANTI_ALIAS_FLAG)
    private val path = Path()
    private var phase = 0f
    private var count = 0
    private var anim: ValueAnimator? = null
    private val ink = Color.rgb(13,16,32)

    fun setCount(value: Int) {
        count = value
        invalidate()
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        if (ValueAnimator.areAnimatorsEnabled()) {
            anim = ValueAnimator.ofFloat(0f,1f).apply {
                duration = 2600; repeatCount = ValueAnimator.INFINITE
                interpolator = AccelerateDecelerateInterpolator()
                addUpdateListener { phase = it.animatedValue as Float; invalidate() }
                start()
            }
        }
    }
    override fun onDetachedFromWindow() { anim?.cancel(); anim = null; super.onDetachedFromWindow() }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val w = width.toFloat(); val h = height.toFloat()
        val s = minOf(w/240f, h/214f)
        canvas.save()
        canvas.translate((w-240f*s)/2, (h-214f*s)/2)
        canvas.scale(s,s)
        val bob = sin(phase * 2*PI).toFloat()*4f

        // Soft illustrated halo
        p.color = Color.argb(24, 179,255,114)
        canvas.drawCircle(120f,100f,94f,p)
        p.color = Color.argb(46,145,123,255)
        canvas.drawCircle(120f,100f,74f,p)
        canvas.save(); canvas.translate(0f,bob)

        // Shadow and feet
        p.color = Color.argb(45,0,0,0); canvas.drawOval(RectF(60f,185f,180f,200f),p)
        p.color = ink
        canvas.drawRoundRect(RectF(78f,158f,101f,190f),10f,10f,p)
        canvas.drawRoundRect(RectF(143f,158f,166f,190f),10f,10f,p)

        val body = when {
            count < 25 -> Color.rgb(179,255,114)
            count < 75 -> Color.rgb(255,210,98)
            count < 150 -> Color.rgb(255,127,189)
            else -> Color.rgb(157,142,255)
        }
        p.color = body
        path.reset()
        // Round lumpy original cloud body
        path.moveTo(62f,146f)
        path.cubicTo(29f,135f,31f,92f,56f,79f)
        path.cubicTo(39f,54f,66f,30f,91f,40f)
        path.cubicTo(103f,18f,140f,18f,151f,40f)
        path.cubicTo(181f,29f,204f,57f,185f,79f)
        path.cubicTo(213f,98f,207f,138f,177f,146f)
        path.cubicTo(170f,176f,74f,177f,62f,146f)
        path.close()
        canvas.drawPath(path,p)
        p.style=Paint.Style.STROKE; p.strokeWidth=5f; p.color=ink; canvas.drawPath(path,p); p.style=Paint.Style.FILL

        // Creature spiral = brand distinction
        p.color=Color.argb(70,13,16,32)
        p.style=Paint.Style.STROKE; p.strokeWidth=3f
        path.reset(); path.moveTo(105f,52f)
        path.cubicTo(92f,70f,127f,82f,142f,65f)
        canvas.drawPath(path,p); p.style=Paint.Style.FILL

        // face
        p.color=ink
        canvas.drawCircle(91f,111f,6.5f,p); canvas.drawCircle(153f,111f,6.5f,p)
        p.style=Paint.Style.STROKE; p.strokeWidth=3.8f; p.strokeCap=Paint.Cap.ROUND
        path.reset(); path.moveTo(104f,130f)
        if (count < 75) path.quadTo(122f,146f,140f,130f)
        else path.quadTo(122f,121f,140f,132f)
        canvas.drawPath(path,p); p.style=Paint.Style.FILL

        if (count >= 75) {
            p.color=ink; p.strokeWidth=3f; p.style=Paint.Style.STROKE
            path.reset(); path.moveTo(151f,41f); path.lineTo(140f,62f); path.lineTo(153f,76f); path.lineTo(142f,94f)
            canvas.drawPath(path,p); p.style=Paint.Style.FILL
        }
        if (count >= 150) {
            p.color=Color.argb(160,13,16,32); p.strokeWidth=4f; p.style=Paint.Style.STROKE
            canvas.drawLine(61f,114f,87f,146f,p); p.style=Paint.Style.FILL
        }
        canvas.restore()
        p.color=Color.rgb(179,255,114)
        canvas.drawCircle(35f,53f,3.5f,p); canvas.drawCircle(210f,130f,4f,p)
        canvas.restore()
    }
}
