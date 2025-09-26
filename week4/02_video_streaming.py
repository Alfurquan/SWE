"""
Week 4 - Mock Interview 2: Video Streaming Platform
Difficulty: Hard | Time Limit: 90 minutes | Google L5 Full System Implementation

PROBLEM STATEMENT:
Design video streaming platform backend (like YouTube/Netflix)

CORE FEATURES:
- Video upload and processing
- Adaptive bitrate streaming
- Content recommendation system
- User subscriptions and playlists
- Live streaming support
- Global content delivery

OPERATIONS:
- uploadVideo(user_id, video_data, metadata): Upload and process video
- streamVideo(video_id, quality): Get streaming URL
- getRecommendations(user_id, limit): Get personalized recommendations
- createPlaylist(user_id, name, videos): Create playlist
- startLiveStream(user_id, title): Start live broadcast
- getAnalytics(video_id): Get view statistics

REQUIREMENTS:
- Support multiple video formats (mp4, webm, etc.)
- Adaptive bitrate streaming (240p to 4K)
- Global CDN distribution
- Real-time analytics and metrics
- Content moderation and copyright
- Mobile and web client support

SYSTEM COMPONENTS:
- Video transcoding pipeline
- CDN and edge caching
- Recommendation ML models
- Real-time streaming infrastructure
- Analytics data pipeline

REAL-WORLD CONTEXT:
YouTube architecture, Netflix streaming, Twitch live streaming, TikTok video delivery

FOLLOW-UP QUESTIONS:
- Video encoding optimization?
- Copyright detection algorithms?
- Live stream latency minimization?
- Regional content restrictions?
- Monetization and ad insertion?

EXPECTED INTERFACE:
video_platform = VideoStreamingPlatform()
video_id = video_platform.uploadVideo("creator1", video_data, metadata)
stream_url = video_platform.streamVideo(video_id, quality="1080p")
recommendations = video_platform.getRecommendations("user1", limit=20)
playlist_id = video_platform.createPlaylist("user1", "Favorites", [video_id])
analytics = video_platform.getAnalytics(video_id)
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
