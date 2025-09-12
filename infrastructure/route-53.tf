data "aws_route53_zone" "main" {
  name         = var.domain_name 
  private_zone = false
}

# Apex domain (talk-to-my-ai.click)
resource "aws_route53_record" "alb_apex" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.domain_name        
  type    = "A"                    
  alias {
    name                   = aws_lb.ai_assistant_alb.dns_name
    zone_id                = aws_lb.ai_assistant_alb.zone_id
    evaluate_target_health = true
  }
}

# WWW subdomain (www.talk-to-my-ai.click)
resource "aws_route53_record" "alb_www" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "www"                 # Subdomain
  type    = "CNAME"               # CNAME allowed for subdomains
  ttl     = 300
  records = [aws_lb.ai_assistant_alb.dns_name]
}

