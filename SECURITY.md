# GCAPI Backend Security

[Refer to GCAPI SECURITY.md in the parent pepository](https://github.com/joeygrable94/GCAPI/blob/main/SECURITY.md)

## Encryption and Hashing Lengths

------------------------------------------------------------

             1  ->  384         =  384.0
            10  ->  384         =  38.4
           100  ->  512         =  5.12
          1000  ->  1708        =  1.708
         10000  ->  13720       =  1.372
        100000  ->  133720      =  1.3372
       1000000  ->  1333720     =  1.33372
      10000000  ->  13333720    =  1.333372
     100000000  ->  133333720   =  1.3333372
    1000000000  ->  1333333720  =  1.33333372

------------------------------------------------------------

       16   ->  408             = 25.5
       32   ->  428             = 13.375
      255   ->  704             = 2.76078431372549
     1024   ->  1752            = 1.7109375
     2048   ->  3116            = 1.521484375
     5000   ->  7040            = 1.408
    45000   ->  60376           = 1.3416888888888888
    65535   ->  87744           = 1.3388876173037307

------------------------------------------------------------

## DB Model Field Encryption Lengths

User

- auth_id: 255
- email: 1024
- username: 255
- picture: 1024

Client

- title: 255
- description: 5000

BDX Feed

- username: 255
- password: 255
- serverhost: 255

Client Bucket

- bucket_name: 255
- object_key: 2048
- description: 5000

Client Report

- title: 255
- url: 2048
- description: 5000

GA4 Property

- title: 255
- measurement_id: 16
- property_id: 16

GA4 Stream

- title: 255
- stream_id: 16

GO Cloud

- project_name: 255
- api_key: 255
- project_id: 255
- project_number: 255
- service_account: 255

GO Search Property

- title: 255

IP Address

- address: 255
- isp: 255
- location: 255

Notes

- title: 255
- description: 5000

SharpSpring

- api_key: 255
- secret_key: 255

Website

- domain: 255

Website Map

- url: 2048

Website Page

- url: 2048
