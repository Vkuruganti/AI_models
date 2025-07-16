provider "aws" {
  region = "us-east-1"
}

resource "aws_msk_cluster" "k8s_metrics" {
  cluster_name           = "k8s-metrics"
  kafka_version          = "2.8.1"
  number_of_broker_nodes = 2
  broker_node_group_info {
    instance_type   = "kafka.m5.large"
    client_subnets  = ["subnet-xxxx", "subnet-yyyy"]
    security_groups = ["sg-xxxx"]
  }
}

resource "aws_lambda_function" "advisor" {
  function_name = "k8s-advisor"
  handler       = "handler.lambda_handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "lambda_app.zip"
  environment {
    variables = {
      KAFKA_BROKER = aws_msk_cluster.k8s_metrics.bootstrap_brokers
      KAFKA_TOPIC  = "k8s-metrics"
    }
  }
  vpc_config {
    subnet_ids         = ["subnet-xxxx", "subnet-yyyy"]
    security_group_ids = ["sg-xxxx"]
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_api_gateway_rest_api" "advisor_api" {
  name        = "advisor-api"
  description = "API Gateway for K8s Advisor"
} 