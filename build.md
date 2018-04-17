# Useful Build Commands

##### Build Package
`python3.6 setup.py sdist`

##### Upload Package
`twine upload dist/*`

##### Fix Common Docker Error
```
ERROR: for evernode-development  Cannot start service evernode-development: b'driver failed programming external connect
ivity on endpoint evernode-development (00f51c8f56a8a9190c88f5b4c0e12d654e89c0001c117e69707cb1b9521b9ee7): Error startin
g userland proxy: mkdir /port/tcp:0.0.0.0:443:tcp:some_ip:443: input/output error'
```
* Step 1
`docker stop $(docker ps -a -q)`
* Step 2
restart docker
* Step 3
try running docker-compose again

# Useful commands to run evernode tests locally without docker
run the docker python install commands.
`wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py`


# Useful Libs
* OTP HMAC-based (HOTP) and time-based (TOTP) passwords - https://github.com/tadeck/onetimepass/
* OAuth 1.0/a & OAuth 2.0 - https://github.com/litl/rauth