## Current Features
- Health check endpoint
- Create job posting (POST /jobs)
- List job postings (GET /jobs)
- Execute Jobs in parallel threads
- Swagger API documentation

## Current Bugs
### A job can be left in running state if
- Executor.submit fails(possible during shutdown or if os does not provide resources)
- Worker crash mid execution
- Database i/o not atomic
