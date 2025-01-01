FROM postgres:latest

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/