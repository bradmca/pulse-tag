# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in PulseTag, please report it to us privately before disclosing it publicly.

### How to Report

- Send an email to: security@pulsetag.dev
- Use the subject line: "Security Vulnerability Report - [Brief Description]"
- Include as much detail as possible about the vulnerability
- Provide steps to reproduce if applicable
- Do not disclose the vulnerability publicly until we have had a chance to address it

### What to Include

- Type of vulnerability (e.g., XSS, SQL injection, etc.)
- Potential impact of the vulnerability
- Detailed steps to reproduce
- Any screenshots or proof-of-concept code
- Your name/handle for credit (optional)

### Response Time

We will acknowledge receipt of your vulnerability report within 48 hours and provide a detailed response within 7 days regarding the next steps.

### Security Measures

PulseTag takes security seriously. Here are some of the measures we have in place:

- Input validation and sanitization
- CORS configuration
- Environment variable protection
- Regular dependency updates
- Container security best practices

### Security Best Practices for Users

1. **API Keys**: Never share your OpenRouter API key or commit it to version control
2. **Docker**: Keep Docker updated to the latest version
3. **Network**: Run the application in a trusted network environment
4. **Cookies**: If using LinkedIn cookies, store them securely and rotate them regularly

### Bug Bounty Program

We appreciate responsible disclosure. While we don't currently offer a formal bug bounty program, we will:

- Credit you in our security advisories
- Provide a shout-out on our social media
- Send some PulseTag swag (when available)

Thank you for helping keep PulseTag and our users safe!
