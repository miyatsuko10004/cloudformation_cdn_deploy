# cloudformation_cdn_deploy
CloudFormationでCDNのディストリビューションを作成、ACMで証明書も発行する

## 手順
* CloudFormationにスタックを作成（cdn-deploy.yaml）
  - リージョンはus-east-1

* lambda関数を作成（lambda_check_acm_issue.py）
  - ACM証明書の発行（ステータスがISSUED）を待機するカスタムリソース
  - IAMロールを作成してアタッチ
    - AWSLambdaBasicExecutionRole
    - AmazonACMReadOnly

## 実行手順
* CloudFormationでcdn-deployを実行
  - パラメーターを入力する
    - DomainName:CDNディストリビューション作成したいドメイン名(example.com)
    - HostedZoneId:上記ドメインのZoneId(Route53で確認)
    - ExistingALBDNSName:オリジンのALBのDNS名(〇〇.ap-northeast-1.elb.amazonaws.com)
  

