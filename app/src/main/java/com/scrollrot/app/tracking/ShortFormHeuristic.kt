package com.scrollrot.app.tracking

import android.view.accessibility.AccessibilityNodeInfo
import java.util.ArrayDeque
import java.util.Locale

/**
 * Experimental UI heuristic: NOT a verified platform reel detector.
 * Analyze only named supported packages, retain no view text or content.
 * Real release requires per-platform adapters & device-specific validation.
 */
object ShortFormHeuristic {
    fun platform(pkg: String): String? = when(pkg) {
        "com.instagram.android", "com.instagram.lite" -> "instagram"
        "com.google.android.youtube" -> "youtube"
        "com.facebook.katana", "com.facebook.lite" -> "facebook"
        "com.snapchat.android" -> "snapchat"
        else -> null
    }

    fun likelyShortFeed(root: AccessibilityNodeInfo?, platform: String): Boolean {
        if (root == null) return false
        val queue = ArrayDeque<AccessibilityNodeInfo>()
        queue.add(root)
        var inspected = 0
        var title = false
        var controlKinds = 0
        var like = false; var comment = false; var share = false
        val tag = when(platform) {
            "instagram", "facebook" -> "reels"
            "youtube" -> "shorts"
            "snapchat" -> "spotlight"
            else -> return false
        }
        while (queue.isNotEmpty() && inspected++ < 100) {
            val node = queue.removeFirst()
            val text = (node.text?.toString().orEmpty() + " " + node.contentDescription?.toString().orEmpty())
                .lowercase(Locale.ROOT).trim()
            if (text == tag || text.startsWith("$tag ")) title = true
            if ("like" in text) like = true
            if ("comment" in text || "reply" in text) comment = true
            if ("share" in text || "send" in text) share = true
            for (i in 0 until node.childCount) node.getChild(i)?.let { queue.addLast(it) }
        }
        controlKinds = listOf(like,comment,share).count { it }
        return title && controlKinds >= 2
    }
}
