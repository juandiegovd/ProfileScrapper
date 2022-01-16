from .media_scrappers.github_scrapper import GitHubScrapper
from .models import GitHubProfile, LinkedinProfile, LinkedinSkill, LinkedinJob
from .media_scrappers.linkedin_scrapper import LinkedinScrapper

git_root_api = "https://api.github.com"
dulanto_profile = "https://www.linkedin.com/in/rodrigodulanto/"
jd_profile = "https://www.linkedin.com/in/juan-diego-villegas-diaz-50b458219/"


def get_profile(user_name):
    profile = GitHubProfile.objects.get_or_create(name=user_name)[0]
    return profile


def get_linkedin_profile(url):
    s = LinkedinScrapper(linkedin_username="mataj2209@gmail.com",
                         linkedin_password="fullstackoverflow",
                         profile_url=dulanto_profile,
                         headless=False)

    s.start()

    s.join()

    # print(s.result.profile.reprJSON())
    gt = GitHubScrapper()
    github = gt.get_by_username("rdulantoc")
    profile_raw = s.result.profile
    (profile, _) = LinkedinProfile.objects.get_or_create(name=profile_raw.name,
                                                         img_src=profile_raw.image_src,
                                                         current_location=profile_raw.current_location,
                                                         email=profile_raw.email)
    _get_skills(profile, profile_raw.skills)
    _get_jobs(profile, profile_raw.jobs)
    return profile


def _get_skills(profile, skills_raw):
    for item in skills_raw:
        skill = LinkedinSkill(name=item)
        skill.save()
        profile.skills.add(skill)

    print(profile.skills.all())


def _get_jobs(profile, jobs_raw):
    for item in jobs_raw:
        job = LinkedinJob(designation=item["designation"],
                          company=item["company"],
                          company_url=item["company_url"],
                          company_image_url=item["company_image_url"],
                          area=item["area"],
                          from_month=item["from_month"],
                          from_year=item["from_year"],
                          to_month=item["to_month"],
                          to_year=item["to_year"])
        job.save()
        profile.jobs.add(job)

