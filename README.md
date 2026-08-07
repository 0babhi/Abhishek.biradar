<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# VPC Monitoring with Flow Logs

<img width="678" height="731" alt="image" src="https://github.com/user-attachments/assets/f522df42-c371-4304-a9ca-a9de89c281c7" />


**Project Link:** [View Project](http://nextwork.ai/projects/aws-networks-monitoring)

**Author:** abhi0b@duck.com  
**Email:** abhi0b@duck.com

---

## VPC Monitoring with Flow Logs

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_3e1e79a1)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon VPC is...is an isolated cloud where we can test the aws services  without being in main network and it is useful because...

### How I used Amazon VPC in this project

In today's project, I used Amazon VPC to...vpc peering

### One thing I didn't expect in this project was...

One thing I didn't expect in this project was...log insight and query

### This project took me...

This project took me...60 min

---

## In the first part of my project...

### Step 1 - Set up VPCs

In this step, I will... because...Create two VPCs from scratch!

to create vpc flow logs

### Step 2 - Launch EC2 instances

In this step, I will...spun up ec2 instance  because...we can ping the ec2 instance in diffenet instances can chcek logs

### Step 3 - Set up Logs

In this step, I will... because...Set up a way to track all inbound and outbound network traffic.

Set up a space that stores all of these records.



### Step 4 - Set IAM permissions for Logs

In this step, I will... because...Give VPC Flow Logs the permission to write logs and send them to CloudWatch.

Finish setting up your subnet's flow log

---

## Multi-VPC Architecture

I started my project by launching...vpc and using vpc and more and limiting the public subnets to 1 and region to 1so that we can easily chcek the vpc logs for easiness

The CIDR blocks for VPCs 1 and 2 are... They have to be unique because...becoz different areas cannot same pin code    so if i give then same cidr block then there will be dublicate ip which will cpnfuse the network where to flow

### I also launched EC2 instances in each subnet

My EC2 instances' security groups allow... This is because...Choose Add security group rule.



For the new rule's Type, select All ICMP - IPv4.



For the new rule's Source, select 0.0.0.0/0

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_e7fa8775)

---

## Logs

Logs are...ogs are like a diary for your computer systems. They record everything that happens, from users logging in to errors popping up. It's the go-to place to understand what's going on with your systems, troubleshoot problems, and keep an eye on who’s doing what.

Log groups are...Think of a log group as a big folder in AWS where you keep related logs together. Usually, logs from the same source or application will go into the same log group, BUT logs are also region-specific. This means log data gets created and saved in the region it was created, although you can use CloudWatch dashboards to bring together logs from different regions.

### I also set up a flow log for VPC 1

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_e8398869)

---

## IAM Policy and Roles

I created an IAM policy because...iam policies which are set of protocal thet perticular action can be done by the user or njot

I also created an IAM role because this role can acceess that polocy 

A custom trust policy is it allows to access vpc flow logs

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_4334d777)

---

## In the second part of my project...

### Step 5 - Ping testing and troubleshooting

In this step, I will... because...test the vpc logs by pinging both ips one by one

### Step 6 - Set up a peering connection

In this step, I will... because...vpc peering the  bridge for communication between the  vpc   usaully private subnet connection is uses vpc peering for communication

### Step 7 - Analyze flow logs

In this step, I will... because...Review the flow logs recorded aboout VPC 1's public subnet.

Analyse the flow logs to get some tasty insights 👀

---

## Connectivity troubleshooting

My first ping test between my EC2 instances had no replies, which means...i had chnged the security policies added the icmp ip4 allow from everywhere so we can see all the replices

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_99d4ba42)

I could receive ping replies if I ran the ping test using the other instance's public IP address, which means...Receiving ping replies from the public IPv4 address means Instance 2 is correctly configured to respond to ping requests, and Instance 1 can actually communicate with Instance 2 if it traffic goes across the public internet!

---

## Connectivity troubleshooting

Looking at VPC 1's route table, I identified that the ping test with Instance 2's private address failed because...we need to create peering vpc bridge here 

### To solve this, I set up a peering connection between my VPCs

I also updated both VPCs' route tables so that... it can access the cidr block of 10.1.0.0/16

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_7316a13d)

---

## Connectivity troubleshooting

I received ping replies from Instance 2's private IP address! This means... vpc peering conncetion is working we can access ther private ec2 from one vpc to other vpc

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_4ec7821f)

---

## Analyzing flow logs

Flow logs tell us about...An AWS VPC Flow Log record consists of space-separated fields that capture details about IP traffic going to and from network interfaces in your VPC. In the default format, a flow log entry contains the following core components:

For example, the flow log I've captured tells us...version: The VPC Flow Logs version (e.g., 2).

account-id: The AWS account ID for the flow log.

interface-id: The ID of the network interface for which the traffic is recorded (e.g., eni-1234567890abcdef0).

srcaddr: The source IPv4 or IPv6 address.

dstaddr: The destination IPv4 or IPv6 address.

srcport: The source port of the traffic.

dstport: The destination port of the traffic.

protocol: The IANA protocol number of the traffic (e.g., 6 for TCP, 17 for UDP, 1 for ICMP).

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_d116818e)

---

## Logs Insights

Logs Insights is...Logs Insights is a CloudWatch feature that analyzes your logs. In Log Insights, you use queries to filter, process and combine data to help you troubleshoot problems or better understand your network traffic!

I ran the query... This query analyzes...The query "Top 10 byte transfers by source and destination IP addresses" is all about discovering the top 10 biggest data transfers between IP addresses in your network! You'll find out which resources are moving the

![Image](http://nextwork.ai/content_maroon_agile_monkey/uploads/aws-networks-monitoring_3e1e79a1)

---

---
