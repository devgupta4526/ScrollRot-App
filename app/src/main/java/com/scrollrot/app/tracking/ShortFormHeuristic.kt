package com.scrollrot.app.tracking

import android.view.accessibility.AccessibilityNodeInfo
import java.util.ArrayDeque
import java.util.Locale

/**
 * Intelligent, privacy-preserving short-form feed detector for Instagram Reels,
 * YouTube Shorts, Facebook Reels, and Snapchat Spotlight.
 *
 * Retains zero user messages, video captions, or media content. Inspects structural
 * UI controls (like/dislike/comment/share/remix/sound buttons and platform view IDs)
 * to distinguish short-form vertical feeds from standard feeds.
 */
object ShortFormHeuristic {

    fun platform(pkg: String): String? = when (pkg) {
        "com.instagram.android", "com.instagram.lite" -> "instagram"
        "com.google.android.youtube" -> "youtube"
        "com.facebook.katana", "com.facebook.lite" -> "facebook"
        "com.snapchat.android" -> "snapchat"
        else -> null
    }

    fun likelyShortFeed(root: AccessibilityNodeInfo?, platform: String): Boolean {
        if (root == null) return false

        return when (platform) {
            "youtube" -> isYouTubeShorts(root)
            "instagram" -> isInstagramReels(root)
            "facebook" -> isFacebookReels(root)
            "snapchat" -> isSnapchatSpotlight(root)
            else -> false
        }
    }

    private fun isYouTubeShorts(root: AccessibilityNodeInfo): Boolean {
        val queue = ArrayDeque<AccessibilityNodeInfo>()
        queue.add(root)
        var inspected = 0
        var hasShortsId = false
        var hasDislike = false
        var hasRemix = false
        var hasSound = false
        var hasLike = false
        var hasComment = false
        var hasShortsText = false

        while (queue.isNotEmpty() && inspected++ < 120) {
            val node = queue.removeFirst()

            // 1. Check View Resource IDs
            val viewId = node.viewIdResourceName?.lowercase(Locale.ROOT).orEmpty()
            if ("reel" in viewId || "short" in viewId) {
                hasShortsId = true
            }

            // 2. Check Content Descriptions and Text
            val text = (node.text?.toString().orEmpty() + " " + node.contentDescription?.toString().orEmpty())
                .lowercase(Locale.ROOT).trim()

            if ("dislike this video" in text || "dislike" in text) hasDislike = true
            if ("remix" in text) hasRemix = true
            if ("sound" in text || "original sound" in text) hasSound = true
            if ("like this video" in text || "like" in text) hasLike = true
            if ("comment" in text || "reply" in text) hasComment = true
            if (text == "shorts" || text.startsWith("shorts ")) hasShortsText = true

            // Early exit if definitive Shorts signature found
            if (hasShortsId && (hasDislike || hasRemix || hasSound || hasLike)) return true
            if (hasDislike && (hasRemix || hasSound || hasLike || hasComment)) return true

            for (i in 0 until node.childCount) {
                node.getChild(i)?.let { queue.addLast(it) }
            }
        }

        // Strong signature: Shorts ID or presence of distinctive Shorts buttons
        return hasShortsId || (hasDislike && (hasLike || hasComment)) || (hasRemix && hasSound) ||
                (hasShortsText && hasLike && hasComment)
    }

    private fun isInstagramReels(root: AccessibilityNodeInfo): Boolean {
        val queue = ArrayDeque<AccessibilityNodeInfo>()
        queue.add(root)
        var inspected = 0
        var hasClipsOrReelId = false
        var hasLike = false
        var hasComment = false
        var hasShare = false
        var hasAudio = false
        var hasReelsText = false

        while (queue.isNotEmpty() && inspected++ < 120) {
            val node = queue.removeFirst()

            // 1. Check View Resource IDs
            val viewId = node.viewIdResourceName?.lowercase(Locale.ROOT).orEmpty()
            if ("clips" in viewId || "reel" in viewId) {
                hasClipsOrReelId = true
            }

            // 2. Check Content Descriptions and Text
            val text = (node.text?.toString().orEmpty() + " " + node.contentDescription?.toString().orEmpty())
                .lowercase(Locale.ROOT).trim()

            if ("like" in text) hasLike = true
            if ("comment" in text || "reply" in text) hasComment = true
            if ("share" in text || "send" in text) hasShare = true
            if ("audio" in text || "original sound" in text || "song" in text) hasAudio = true
            if (text == "reels" || text.startsWith("reels ")) hasReelsText = true

            if (hasClipsOrReelId && (hasLike || hasComment || hasShare)) return true

            for (i in 0 until node.childCount) {
                node.getChild(i)?.let { queue.addLast(it) }
            }
        }

        return hasClipsOrReelId || (hasReelsText && hasLike && hasComment) ||
                (hasLike && hasComment && hasShare && hasAudio)
    }

    private fun isFacebookReels(root: AccessibilityNodeInfo): Boolean {
        val queue = ArrayDeque<AccessibilityNodeInfo>()
        queue.add(root)
        var inspected = 0
        var hasReelSignature = false
        var controlCount = 0

        while (queue.isNotEmpty() && inspected++ < 80) {
            val node = queue.removeFirst()
            val viewId = node.viewIdResourceName?.lowercase(Locale.ROOT).orEmpty()
            val text = (node.text?.toString().orEmpty() + " " + node.contentDescription?.toString().orEmpty())
                .lowercase(Locale.ROOT).trim()

            if ("reel" in viewId || "fb_shorts" in viewId || "reels" in text) hasReelSignature = true
            if ("like" in text || "comment" in text || "share" in text) controlCount++

            for (i in 0 until node.childCount) {
                node.getChild(i)?.let { queue.addLast(it) }
            }
        }
        return hasReelSignature && controlCount >= 2
    }

    private fun isSnapchatSpotlight(root: AccessibilityNodeInfo): Boolean {
        val queue = ArrayDeque<AccessibilityNodeInfo>()
        queue.add(root)
        var inspected = 0
        var hasSpotlight = false

        while (queue.isNotEmpty() && inspected++ < 80) {
            val node = queue.removeFirst()
            val viewId = node.viewIdResourceName?.lowercase(Locale.ROOT).orEmpty()
            val text = (node.text?.toString().orEmpty() + " " + node.contentDescription?.toString().orEmpty())
                .lowercase(Locale.ROOT).trim()

            if ("spotlight" in viewId || "spotlight" in text) hasSpotlight = true

            for (i in 0 until node.childCount) {
                node.getChild(i)?.let { queue.addLast(it) }
            }
        }
        return hasSpotlight
    }
}
