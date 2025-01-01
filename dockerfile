FROM postgres:latest

# Copy initialization scripts
COPY init.sql .
EXPOSE 5432