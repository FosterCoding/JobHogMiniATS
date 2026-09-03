from dataclasses import dataclass
import requests
import json

@dataclass
class Job:
#Required fields always have to come before the optional fields with defaults
    id: str
    source: str #Greenhouse, Lever or USAJobs
    title: str
    company: str #employer
    location: str
    url: str
    description: str
    remote: bool | None = None #T or F
    pay_min: float | None = None
    pay_max: float | None = None

def greenhouse_jobs(company_name: str) -> list[Job]:  #company_name: str = company_name is annotated as a str -> list[Job] the arrow means "this function returns a list of Job objects"
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_name}/jobs" #API URL here. Assign it to the URL variable
    response = requests.get(url, params={"content": "true"}) #API Request; content true enables the full HTML Job Description, without it, we only get metadata
    response.raise_for_status()#errors if request fails. 200=Success, 404=Not found, 429=Rate limit, 500=Server error
    data = response.json() #Returns API Call with JSON Response. 

    jobs = [] #initialize an empty list
    for info in data["jobs"]: #loops over the data response to organize the data into a readable format. Means go into the dict called data, and give me the value stored under the key "jobs".
        job = Job(
            id=str(info["id"]),
            source="Greenhouse",
            title=info["title"], #pull the title
            location=info["location"], #pull the location
            url=info["url"], #pull the url
            description=info["description"],
        )
        jobs.append(job) #append the jobs list with the information gathered in "job" from for loop
    return jobs


#{One item of the response for testing purposes
 {"absolute_url":"https://stripe.com/jobs/search?gh_jid=7532733","data_compliance":[{"type":"gdpr","requires_consent":false,"requires_processing_consent":false,"requires_retention_consent":false,"retention_period":null,"demographic_data_consent_applies":false}],"education":"education_required","internal_job_id":3336216,"location":{"name":"San Francisco, CA"},"metadata":null,"id":7532733,"updated_at":"2026-08-25T17:40:40-04:00","requisition_id":"See Opening ID","title":"Account Executive, AI Sales","company_name":"Stripe","first_published":"2026-02-03T15:19:01-05:00","language":"en","application_deadline":null}
}