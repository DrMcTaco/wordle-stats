-- Compute the frequesncy distribution of most common scores for a daily puzzle
select 
    modal_score,
    CAST(count(modal_score) as REAL) / CAST((select count(*) from solution_stats) as REAL) as score_freq
from solution_stats
group by modal_score