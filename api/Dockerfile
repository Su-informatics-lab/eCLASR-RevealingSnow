FROM python:3.6-onbuild
MAINTAINER Ryan Barnard "rybarnar@wakehealth.edu"

EXPOSE 5000

ENV PYTHONPATH=/usr/src/app

ENTRYPOINT ["/usr/src/app/bin/entrypoint.sh"]
CMD ["server"]
