resource "aws_dynamodb_table" "conversations" {
  name           = "ai-assistant-conversations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "conversation_id"

  attribute {
    name = "conversation_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  global_secondary_index {
    name            = "timestamp-index"
    hash_key        = "timestamp"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name        = "AI Assistant Conversations"
    Environment = "production"
  }
}

resource "aws_iam_role_policy" "dynamodb_access" {
  name = "dynamodb-conversations-access"
  role = aws_iam_role.app-server-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Resource = [
          aws_dynamodb_table.conversations.arn,
          "${aws_dynamodb_table.conversations.arn}/index/*"
        ]
      }
    ]
  })
}