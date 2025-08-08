# VSCode GitHub Actions Integration Guide

## Overview

The GitHub Actions VSCode extension provides a seamless way to monitor and manage your CI/CD pipeline directly from your development environment.

## Setup Verification

### Check Extension Status
1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "GitHub Actions"
4. Verify it's installed and enabled
5. Check that you're signed in to GitHub

### Verify Permissions
The extension should have:
- ✅ Repository access
- ✅ Workflow permissions
- ✅ Actions permissions

## Using the Extension

### 1. View Workflow Status
1. Open the GitHub Actions panel in VSCode
2. You'll see your "JobTrackerDB CI/CD Pipeline"
3. Click on any workflow run to view details

### 2. Monitor Pipeline Progress
- **Real-time updates** - See job status as they run
- **Log viewing** - Click on any step to see detailed logs
- **Error identification** - Quickly spot failed steps

### 3. Manual Workflow Triggers
1. Right-click on the workflow
2. Select "Run workflow"
3. Choose environment (staging/production)
4. Monitor the execution

### 4. Debug Failed Runs
1. Click on failed workflow
2. Review step-by-step logs
3. Identify the specific failure point
4. Fix the issue locally
5. Push changes to trigger new run

## Integration with Your Pipeline

### Workflow Monitoring
The extension will show:
- ✅ **Backend Tests** - Python testing and linting
- ✅ **Frontend Tests** - React/TypeScript testing
- ✅ **Database Migration** - Alembic validation
- ✅ **Build Process** - Frontend and backend packaging
- ✅ **Deployment** - Staging and production deployments

### Quick Actions
1. **Re-run failed jobs** - Right-click and select "Re-run jobs"
2. **View artifacts** - Download test results and build artifacts
3. **Check secrets** - Verify GitHub secrets are properly configured
4. **Monitor deployments** - Track staging and production deployments

## Troubleshooting

### Common Issues

1. **Extension not showing workflows**
   - Check GitHub authentication
   - Verify repository permissions
   - Refresh the extension

2. **Cannot trigger workflows**
   - Ensure you have write permissions
   - Check branch protection rules
   - Verify workflow file syntax

3. **Logs not loading**
   - Check internet connection
   - Verify GitHub API access
   - Try refreshing the extension

### Debug Steps

1. **Check authentication:**
   - Go to VSCode settings
   - Search for "GitHub"
   - Verify authentication status

2. **Test workflow trigger:**
   - Make a small change to trigger workflow
   - Monitor in VSCode extension
   - Check GitHub Actions tab in browser

3. **Verify permissions:**
   - Go to GitHub repository
   - Settings > Actions > General
   - Check workflow permissions

## Best Practices

### Development Workflow
1. **Local testing first** - Run tests locally before pushing
2. **Monitor in VSCode** - Use extension to watch pipeline
3. **Quick feedback** - See results immediately in editor
4. **Debug efficiently** - Use logs to identify issues

### Pipeline Management
1. **Regular monitoring** - Check pipeline status daily
2. **Proactive fixes** - Address issues before they block development
3. **Performance tracking** - Monitor build times and optimize
4. **Security awareness** - Review security scan results

## Advanced Features

### Custom Notifications
Configure the extension to notify you of:
- ✅ Pipeline failures
- ✅ Deployment completions
- ✅ Security vulnerabilities
- ✅ Performance regressions

### Integration with Other Extensions
- **GitLens** - See commit details in workflow runs
- **Docker** - Monitor container builds
- **Remote Development** - Work with remote repositories

## Security Considerations

1. **Token management** - Use GitHub tokens with minimal permissions
2. **Secret protection** - Never expose secrets in logs
3. **Access control** - Limit who can trigger workflows
4. **Audit trails** - Monitor who triggered what and when 