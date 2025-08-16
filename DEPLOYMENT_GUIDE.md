# 🚀 Deployment Guide - Bulk Image Cropper

Your Flask app is ready for online deployment! Here are the best options:

## 🌟 Option 1: Render (Recommended - FREE)

**Why Render?** Free tier, easy deployment, automatic HTTPS, custom domain support

### Step-by-Step Deployment:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub/GitLab

2. **Connect Your Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository with your code

3. **Configure Service**
   - **Name**: `bulk-image-cropper` (or any name you like)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

## 🌟 Option 2: Railway (Alternative - FREE)

**Why Railway?** Free tier, very fast deployment, good for ML apps

### Steps:
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect it's a Python app
6. Deploy automatically!

## 🌟 Option 3: Heroku (Paid but Reliable)

**Why Heroku?** Very reliable, good documentation, but requires credit card

### Steps:
1. Install Heroku CLI
2. Run these commands:
```bash
heroku create your-app-name
git add .
git commit -m "Ready for deployment"
git push heroku main
```

## 🔧 Important Notes:

### File Storage:
- **Local folders won't work online** - you'll need cloud storage
- Consider using AWS S3, Google Cloud Storage, or similar
- For now, the app will work but uploaded files won't persist

### Dependencies:
- All required packages are in `requirements.txt`
- Gunicorn is added for production deployment
- OpenCV and MediaPipe will work on cloud platforms

### Environment Variables:
- Add any API keys or secrets in your deployment platform's dashboard
- Don't commit sensitive information to your code

## 🚀 Quick Deploy Commands:

### For Render:
1. Push your code to GitHub
2. Connect to Render
3. Deploy automatically

### For Railway:
1. Push your code to GitHub
2. Connect to Railway
3. Deploy automatically

## 📱 After Deployment:

1. **Test your app**: Visit the provided URL
2. **Test upload**: Try uploading an image
3. **Test processing**: Check if cropping works
4. **Monitor logs**: Check for any errors

## 🆘 Troubleshooting:

- **Build fails**: Check if all packages are in `requirements.txt`
- **App crashes**: Check logs in your deployment platform
- **Upload issues**: Check file size limits and permissions

## 🌐 Custom Domain (Optional):

After deployment, you can:
1. Add a custom domain in your platform's dashboard
2. Point your domain's DNS to the provided URL
3. Enable HTTPS automatically

---

**Ready to deploy?** Choose Render (easiest) or Railway (fastest) and follow the steps above!

Your app will be live online in about 10-15 minutes! 🎉
