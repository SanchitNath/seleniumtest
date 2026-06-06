### Steps to run local http server
```
> sudo apt update
> sudo apt install apache2
> sudo mkdir -p /var/www/html/<some name>
> sudo chown -R root:root /var/www/html/<some name>
> sudo rm -rf /var/www/html/index.html
```
---
### Access Cassandara DB
```
> exec into cassandra pod -> kubectl exec -it cassandra-0 -- /bin/sh
> cqlsh -k public
> list of all tables : describe tables; - some fields can be encrypted. 
> describe table <table_name> - to see the table schema.
> Eg query :  select * from auditlog_primary where acct_id =a726b731-069f-4a27-9236-d847cfea0baa;
```
If columns are encrypted transparently (`TDE`) at the database layer, `cqlsh` will show them 
normally to authorized users. If they are encrypted at the application layer before insertion, 
the output will appear as a raw hexadecimal string or binary blob.
---
### How to connect an EC2 instance using RDP
```
> Launch the instance
> Start the instance by clicking on “Instance state”
> Select “Connect”
> Select “RDP client”
> Connection type should be “Connect using RDP client”
> Click on “Download remote desktop file”
> Copy “Public DNS” from here
> Copy “Username” from here
> Click on “Get password” every time to get new password by adding the .pem file and copy it
> Launch Reminna or any other RDP client
> Select new connection profile
> Enter server name as “Public DNS” with username and password
> Click on “Connect” button
> Accept the “Certs”.
```
---
## AWS
### Create a CloudFront distribution in AWS
```
Open the CloudFront console, and then choose Create Distribution.
In Origin domain, enter the name of the bucket that you created in the previous steps.
In S3 bucket access, choose Yes use OAI (bucket can restrict access to only CloudFront).
In Origin access identity, choose Create new OAI, and then choose Create.
Choose Create distribution.
Policy of bucket after creating cloudfront can be updated to :-  
{
    "Sid": "AllowCloudFrontServicePrincipal",
    "Effect": "Allow",
    "Principal": {
        "Service": "cloudfront.amazonaws.com"
    },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::crlnewbucket/*",
    "Condition": {
        "StringEquals": {
            "AWS:SourceArn": "arn:aws:cloudfront::513076507034:distribution/E1MHTVASWTUZ8A"
        }
    }
}
```
### Install root CA under PCA in AWS
```
> Open the created PCA list by going to https://ap-south-1.console.aws.amazon.com/acm-pca/home?region=ap-south-1#/certificateAuthorities?arn=&tab=null.
> Open the desired PCA
> Click on “Actions” button
> Click on “Install CA certificate”
> Set “Validity”,  “Signature algorithm” from dropdown
> Then click on “Confirm and Install”
```
### Issuing private certs in AWS
(If you are using AWS CLI version 1.6.3 or later, use the prefix fileb:// when specifying base64-encoded input files 
such as CSRs. This ensures that AWS Private CA parses the data correctly.)
```
> arn of PCA is in the format : arn:aws:acm-pca:region:account:certificate-authority/CA_ID
> aws configure
> openssl req -out csr.pem -new -newkey rsa:2048 -nodes -keyout private-key.pem
> openssl req -in csr.pem -text -noout
> aws acm-pca issue-certificate --certificate-authority-arn {arn of PCA} --csr fileb:///home/sanchit/csr.pem --signing-algorithm "SHA256WITHRSA" --validity Value=365,Type="DAYS"

> The ARN of the issued certificate is returned:
{
   "CertificateArn":"arn:aws:acm-pca:region:account:certificate-authority/CA_ID/certificate/certificate_ID"
}

> Rerun the last command with different expiration time to get new certs.
> Certs can be downloaded locally → 
$ aws acm-pca get-certificate --certificate-authority-arn {arn of PCA} --certificate-arn {CertificateArn} | jq -r .'Certificate' > cert.pem
```
### Revoked certs in aws
```
> arn of PCA is in the format : arn:aws:acm-pca:region:account:certificate-authority/CA_ID
> serial_number of cert is nothing but CA_ID of it

> Revocation can reason can only be one of [AFFILIATION_CHANGED, CESSATION_OF_OPERATION, A_A_COMPROMISE, 
PRIVILEGE_WITHDRAWN, SUPERSEDED, UNSPECIFIED, KEY_COMPROMISE, CERTIFICATE_AUTHORITY_COMPROMISE]  

> aws acm-pca revoke-certificate --certificate-authority-arn {arn of PCA} --certificate-serial {serial_number} --revocation-reason "KEY_COMPROMISE" 
> It does not return a response.

> A CRL is typically updated approximately 30 minutes after a certificate is revoked. 
If for any reason a CRL update fails, AWS Private CA makes further attempts every 15 minutes.
```
---
## GCP
### Session token in GCP
```
> sudo snap install google-cloud-cli --classic (or) brew install --cask gcloud-cli
> gcloud auth login
> gcloud auth login sanchitnath6@gmail.com --force
> Login into the browser opened with email
> Allow access there
> gcloud auth print-access-token
```
---
### How to remove cache
```
> free -m

> If buff/cache is taking more than 3/4GB, run
sudo sync

> echo 1 | sudo tee /proc/sys/vm/drop_caches
> free -m

> This ensures dirty pages are flushed before clearing cache: 
sync && sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"
```