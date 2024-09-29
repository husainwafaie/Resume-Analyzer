import numpy as np
import pandas as pd
from . import nlp_utils
import random


def calc(resume, job_description): 
    resume_words = set(resume)

    total_words = len(job_description)
    count = 0
    for i in job_description: 
        if i in resume_words: 
            count += 1

    return count/total_words

def pos_feedbacks(mode: bool, words: str): 
    possible = []
    
    if not mode: 
        possible.append(f"Differences: However, the job description emphasizes some areas that are missing 
                        from your resume, including {words}. Consider tailoring your resume to highlight 
                        these areas.")
        
        possible.append(f"Differences: However, the job description emphasizes some areas that are missing 
                        from your resume, including {words}. Consider adding those keywords to your resume.")
        
        possible.append(f"Differences: However, the job description emphasizes some areas that are missing 
                        from your resume, including {words}. Consider adding specific keywords to your resume
                        that align with those keywords.")
        
        possible.append(f"Differences: However, the job description emphasizes some areas that are missing 
                        from your resume, including {words}. Consider adding more relevant keywords to your 
                        resume to maximize your chances of getting an interview.")
        
        possible.append(f"Differences: However, the job description emphasizes some areas that are missing 
                        from your resume, including {words}. Consider 
                        adding more details about these topics to better align with the job requirements.")
        
    else: 
        possible.append(f"Similarities: Your resume matches important areas mentioned in the job description, 
                        such as {words}. This shows that you have relevant experience 
                        in key areas!")
        
        possible.append(f"Similarities: Your resume is a fit for some of the requirements in the 
                        job description, like {words}. Those experiences overlap with the job description!")
        
        possible.append(f"Similarities: Your resume matches important areas mentioned in the job description, 
                        such as {words}. You might be a good fit for this job!")
        
        possible.append(f"Similarities: Your resume matches important areas mentioned in the job description, 
                        such as {words}. Looks like you match some of the key requirements of the job!")
        
        possible.append(f"Similarities: Your resume matches important areas mentioned in the job description, 
                        such as {words}. This shows that you have relevant experience 
                        in key areas!")
        

    index = random.randint(0, len(possible) - 1)
    
    #return a random string from the possible list
    return possible[index]
