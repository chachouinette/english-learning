# Deploying English Learning App to GCP Cloud Run

This guide will walk you through deploying your English Learning web application to Google Cloud Platform (GCP) using Cloud Run.

## Prerequisites

1. A GCP account (get $300 free credits for new users at https://cloud.google.com)
2. Google Cloud SDK installed on your machine
3. Docker installed (optional, for local testing)

## Setup Instructions

### 1. Install Google Cloud SDK

If you haven't already, install the Google Cloud SDK:

**macOS:**
```bash
brew install google-cloud-sdk
```

**Or download from:** https://cloud.google.com/sdk/docs/install

### 2. Initialize and Login to GCP

```bash
# Login to your GCP account
gcloud auth login

# Set your project (replace PROJECT_ID with your actual project ID)
gcloud config set project PROJECT_ID

# If you don't have a project yet, create one:
# gcloud projects create PROJECT_ID --name="English Learning App"
```

### 3. Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com
```

### 4. Deploy to Cloud Run

Cloud Run can build your container automatically! Just run:

```bash
# Deploy directly from source (easiest method)
gcloud run deploy english-learning-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi

# Or if you prefer to build the container first:
# gcloud builds submit --tag gcr.io/PROJECT_ID/english-learning-app
# gcloud run deploy english-learning-app \
#   --image gcr.io/PROJECT_ID/english-learning-app \
#   --platform managed \
#   --region us-central1 \
#   --allow-unauthenticated
```

### 5. Access Your App

After deployment completes, Cloud Run will provide a URL like:
```
https://english-learning-app-xxxxx-uc.a.run.app
```

Visit this URL in your browser to use your app!

## Testing Locally First

Before deploying, you can test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

# Visit http://localhost:8080 in your browser
```

Or test with Docker:

```bash
# Build the Docker image
docker build -t english-learning-app .

# Run the container
docker run -p 8080:8080 english-learning-app

# Visit http://localhost:8080 in your browser
```

## Important Notes

### Data Persistence

Currently, the app uses a local JSON file (`vocabulary.json`) to store words. This means:

- **Data will reset** when the Cloud Run instance restarts
- Each deployment will start with the original vocabulary.json file

### Solutions for Data Persistence:

**Option 1: Cloud Storage (Recommended)**
- Store vocabulary.json in a Cloud Storage bucket
- Modify app.py to read/write from Cloud Storage

**Option 2: Cloud Firestore**
- Use Firestore as a NoSQL database
- More complex but better for production

**Option 3: Persistent Disk (Cloud Run volumes)**
- Mount a persistent disk to Cloud Run
- Available in newer Cloud Run versions

### Updating Your App

To redeploy after making changes:

```bash
gcloud run deploy english-learning-app \
  --source . \
  --platform managed \
  --region us-central1
```

### Monitoring and Logs

View logs:
```bash
gcloud run services logs read english-learning-app --region us-central1
```

View service details:
```bash
gcloud run services describe english-learning-app --region us-central1
```

### Cost Estimation

Cloud Run pricing (as of 2025):
- First 2 million requests per month: FREE
- 360,000 GB-seconds of memory: FREE
- 180,000 vCPU-seconds: FREE

For a small learning app with moderate usage, you'll likely stay within the free tier!

### Cleanup (Delete Resources)

To delete the service and stop incurring charges:

```bash
gcloud run services delete english-learning-app --region us-central1
```

## Troubleshooting

### Issue: "Permission denied"
- Make sure you're logged in: `gcloud auth login`
- Check your project: `gcloud config get-value project`

### Issue: "API not enabled"
- Enable required APIs as shown in step 3

### Issue: App doesn't load
- Check logs: `gcloud run services logs read english-learning-app`
- Verify the container builds locally first

### Issue: Lost vocabulary data
- This is expected! Implement one of the persistence solutions mentioned above

## Next Steps

1. Set up data persistence using Cloud Storage or Firestore
2. Add authentication to protect your vocabulary
3. Set up a custom domain
4. Configure CI/CD for automatic deployments

## Support

For GCP-specific issues, visit: https://cloud.google.com/run/docs
