import instaloader

def get_profile_data(username):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            'username': profile.username,
            'followers': profile.followers,
            'followees': profile.followees,
            'is_private': profile.is_private,
            'is_verified': profile.is_verified,
            'bio': profile.biography,
            'posts': profile.mediacount,
        }
    except Exception as e:
        print(f"Error: {e}")
        return None
