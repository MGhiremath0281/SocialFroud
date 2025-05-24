def is_suspicious(profile):
    reasons = []
    if profile['followers'] < 50 and profile['followees'] > 500:
        reasons.append("High following-to-follower ratio")
    if not profile['bio']:
        reasons.append("Empty bio")
    if profile['posts'] == 0:
        reasons.append("No posts on profile")
    if profile['is_private']:
        reasons.append("Private profile")
    if not profile['is_verified'] and profile['followers'] > 5000 and profile['followees'] < 50:
        reasons.append("Unverified account with large followers and low followees")
    
    return (len(reasons) > 0, reasons)
