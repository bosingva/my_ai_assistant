# Verify your domain in SES
resource "aws_ses_domain_identity" "main" {
  domain = var.domain_name
}

# Verify your email address
resource "aws_ses_email_identity" "dimitri_email" {
  email = "korgalidzed@gmail.com"
}

# Create DKIM records for domain authentication
resource "aws_ses_domain_dkim" "main" {
  domain = aws_ses_domain_identity.main.domain
}

# Add DKIM records to Route 53
resource "aws_route53_record" "ses_dkim" {
  count   = 3
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "${aws_ses_domain_dkim.main.dkim_tokens[count.index]}._domainkey.${var.domain_name}"
  type    = "CNAME"
  ttl     = 600
  records = ["${aws_ses_domain_dkim.main.dkim_tokens[count.index]}.dkim.amazonses.com"]
}

# Add SPF record
resource "aws_route53_record" "ses_spf" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "TXT"
  ttl     = 600
  records = ["v=spf1 include:amazonses.com ~all"]
}

# Grant EC2 instances permission to send emails
resource "aws_iam_role_policy" "ses_access" {
  name = "ses-email-access"
  role = aws_iam_role.app-server-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "*"
      }
    ]
  })
}