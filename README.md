# InstaFroud 🔍

**InstaFroud** is a Flask-based web application designed to detect potentially fake Instagram accounts. It uses Instagram scraping combined with custom fraud detection logic and OTP-based verification to assess account authenticity.

## 🔧 How It Works

1. **Profile Scraping**: Uses `instaloader` to extract public Instagram data such as username, followers, following, post count, and bio.
2. **Fraud Detection Logic**: Analyzes:
   - Follower to following ratio
   - Account privacy (private/public)
   - Post count
   - Bio content (suspicious keywords, emojis, etc.)
3. **OTP Verification**: Implements Twilio-based OTP authentication to validate user identity before displaying results.

## 🚀 How to Use

1. Enter the Instagram username you want to analyze.
2. Provide your phone number to receive an OTP.
3. Verify the OTP sent via Twilio.
4. View the analysis result showing whether the account is likely real or fake, based on multiple profile factors.

## 💻 Cloning and Running the Project

```bash
# Step 1: Clone the repository
git clone https://github.com/MGhiremath0281/InstaFroud.git
cd InstaFroud

# Step 2: Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Set environment variables (Twilio SID, Auth Token, etc.)
# Example:
export TWILIO_ACCOUNT_SID=your_sid
export TWILIO_AUTH_TOKEN=your_token
export TWILIO_PHONE_NUMBER=your_twilio_number

# Step 5: Run the application
 streamlit run app.py
