# CIDE Deployment Guide

## 🚀 Hosting Options

### Option 1: Render.com (Recommended - FREE)

**Best for:** Quick deployment, free hosting, automatic SSL

#### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Sign up at Render.com**
   - Go to https://render.com
   - Sign up with GitHub account

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (Anorak001/CIDE)
   - Render will auto-detect the `render.yaml` file

4. **Configure (Auto-filled from render.yaml)**
   - Name: `cide`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

5. **Add Environment Variable** (Optional)
   - Key: `SECRET_KEY`
   - Value: Generate random string (e.g., `python -c "import secrets; print(secrets.token_hex(32))"`)

6. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes for build
   - Your app will be live at: `https://cide-xxxx.onrender.com`

**Free Tier Limits:**
- ✅ 750 hours/month (enough for 24/7)
- ✅ Automatic SSL
- ✅ Custom domain support
- ⚠️ Spins down after 15 min inactivity (30s cold start)

---

### Option 2: Railway.app (Easy - $5/month)

**Best for:** No cold starts, better performance

#### Steps:

1. **Push to GitHub** (if not done)

2. **Deploy to Railway**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your CIDE repository

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `SECRET_KEY`
   - Deploy automatically happens

4. **Get URL**
   - Click "Generate Domain"
   - Your app: `https://cide.up.railway.app`

**Pricing:**
- $5/month for hobby plan
- No cold starts
- Better performance

---

### Option 3: PythonAnywhere (FREE with limits)

**Best for:** Simple Python hosting, no credit card needed

#### Steps:

1. **Sign up**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Code**
   ```bash
   # On PythonAnywhere bash console:
   git clone https://github.com/Anorak001/CIDE.git
   cd CIDE
   pip3 install --user -r requirements.txt
   ```

3. **Configure Web App**
   - Go to "Web" tab
   - Add new web app
   - Choose Flask
   - Set source code: `/home/yourusername/CIDE`
   - Set working directory: `/home/yourusername/CIDE`
   - Set WSGI file to point to `app.py`

4. **Reload**
   - Click green reload button
   - Visit: `https://yourusername.pythonanywhere.com`

**Free Tier Limits:**
- ✅ One web app
- ✅ 512MB storage
- ⚠️ CPU seconds limited
- ⚠️ Custom domain requires paid plan

---

### Option 4: Heroku (Classic - $5-7/month)

**Best for:** Enterprise-ready, lots of addons

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # Windows (via Chocolatey)
   choco install heroku-cli
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create cide-plagiarism-detector
   git push heroku main
   heroku open
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ```

**Pricing:**
- $5-7/month for eco dynos
- No cold starts with higher tiers
- Professional features

---

### Option 5: DigitalOcean App Platform ($5/month)

**Best for:** Scalable, professional deployment

#### Steps:

1. **Sign up** at https://www.digitalocean.com

2. **Create App**
   - Go to "Apps" → "Create App"
   - Connect GitHub repository
   - Choose: CIDE repository

3. **Configure**
   - Auto-detects Python
   - Build: `pip install -r requirements.txt`
   - Run: `gunicorn app:app`

4. **Deploy**
   - Add environment variables
   - Click "Create Resources"
   - Wait 5 minutes

**Pricing:**
- $5/month basic plan
- $12/month for better performance
- Scalable infrastructure

---

### Option 6: Vercel (Serverless - FREE)

**Best for:** Serverless deployment, instant deploys

#### Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### Steps:
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts
4. Done! Deployed at: `https://cide.vercel.app`

**Free Tier:**
- ✅ Unlimited deployments
- ✅ Automatic SSL
- ✅ Custom domains
- ⚠️ Serverless limitations (execution time)

---

## 🔧 Production Checklist

Before deploying, ensure:

- [ ] Secret key uses environment variable
- [ ] Debug mode is OFF in production
- [ ] HTTPS enabled (automatic with most hosts)
- [ ] Error logging configured
- [ ] File upload limits appropriate
- [ ] CORS configured if needed

### Update app.py for production:

```python
# At the bottom of app.py, change:
if __name__ == '__main__':
    # Development
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    else:
        app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

---

## 🎯 My Recommendation

**For Portfolio/Demo:** Use **Render.com** (Free)
- ✅ Easy setup (5 minutes)
- ✅ Free forever
- ✅ Automatic deploys from GitHub
- ✅ Professional URL
- ⚠️ Only downside: 30s cold start after inactivity

**For Production:** Use **Railway.app** ($5/month)
- ✅ No cold starts
- ✅ Better performance
- ✅ Easy scaling
- ✅ Professional features

---

## 📝 Quick Deploy to Render (Step-by-step)

1. **Commit changes**
   ```bash
   git add .
   git commit -m "Add deployment config"
   git push origin main
   ```

2. **Go to Render.com**
   - Sign up with GitHub
   - Click "New +" → "Web Service"

3. **Connect repository**
   - Search for "CIDE"
   - Click "Connect"

4. **Deploy**
   - Name: `cide-plagiarism-detector`
   - Branch: `main`
   - Build: Auto-detected from render.yaml
   - Click "Create Web Service"

5. **Wait 2-3 minutes**
   - Watch build logs
   - Get your URL: `https://cide-plagiarism-detector.onrender.com`

6. **Test**
   - Visit your URL
   - Upload files
   - Download reports
   - Try batch comparison

7. **Share!**
   - Add URL to GitHub README
   - Share on LinkedIn
   - Add to portfolio

---

## 🔗 Custom Domain (Optional)

Most hosts support custom domains:

1. **Buy domain** (e.g., GoDaddy, Namecheap)
2. **Add CNAME record:**
   - Name: `cide` or `@`
   - Value: Your host's domain
3. **Configure in hosting platform**
4. **Wait for DNS propagation** (24-48 hours)

Example: `https://cide.yourdomain.com`

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid | Cold Starts | Best For |
|----------|-----------|------|-------------|----------|
| Render.com | ✅ Yes | $7/mo | Yes (30s) | Portfolio |
| Railway | ❌ No | $5/mo | No | Production |
| PythonAnywhere | ✅ Yes | $5/mo | No | Simple hosting |
| Heroku | ❌ No | $7/mo | No | Enterprise |
| DigitalOcean | ❌ No | $5/mo | No | Scalable |
| Vercel | ✅ Yes | $20/mo | No | Serverless |

---

## 🆘 Troubleshooting

### Issue: "Application failed to start"
**Solution:** Check build logs, ensure `gunicorn` is in requirements.txt

### Issue: "Module not found"
**Solution:** Add missing package to `requirements.txt`

### Issue: "500 Internal Server Error"
**Solution:** Check application logs, turn on debug mode temporarily

### Issue: "Cold start is slow"
**Solution:** 
- Upgrade to paid plan (no cold starts)
- Use a cron job to ping your app every 10 minutes

---

## 🎉 You're Ready to Deploy!

Choose your hosting platform and follow the steps above. For a quick portfolio demo, **I recommend Render.com** - you can have CIDE live in under 5 minutes!

Need help? Check the platform-specific documentation or ask for assistance.
