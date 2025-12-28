with revenues as (
 select *
 from studied-brand-481913-u8.staging_db.stg_payment
)

, reporting_dates as (
  select *
  from studied-brand-481913-u8.reporting_db.reporting_periods_table
  where reporting_period in ('Day', 'Month', 'Year')
)

, revenues_per_period as (
 select
  'Day' as reporting_period
  , date_trunc(revenues.payment_payment_date, day) as reporting_date
  , sum(revenues.payment_amount) as total_revenues
 from revenues
 group by 1,2
union all
 select
  'Month' as reporting_period
  , date_trunc(revenues.payment_payment_date, month) as reporting_date
  , sum(revenues.payment_amount) as total_revenues
 from revenues
 group by 1,2
union all
 select
  'Year' as reporting_period
  , date_trunc(revenues.payment_payment_date, year) as reporting_date
  , sum(revenues.payment_amount) as total_revenues
 from revenues
 group by 1,2
)

, final as (
select
  reporting_dates.reporting_period
  , reporting_dates.reporting_date
  , coalesce(revenues_per_period.total_revenues,0) as total_revenues
 from reporting_dates
left join revenues_per_period
on reporting_dates.reporting_period = revenues_per_period.reporting_period
and reporting_dates.reporting_date = revenues_per_period.reporting_date
where reporting_dates.reporting_period = 'Day'
union all
select
 reporting_dates.reporting_period
 , reporting_dates.reporting_date
 , coalesce(revenues_per_period.total_revenues,0) as total_revenues
from reporting_dates
left join revenues_per_period
on reporting_dates.reporting_period = revenues_per_period.reporting_period
and reporting_dates.reporting_date = revenues_per_period.reporting_date
where reporting_dates.reporting_period = 'Month'
union all
select
 reporting_dates.reporting_period
 , reporting_dates.reporting_date
 , coalesce(revenues_per_period.total_revenues,0) as total_revenues
from reporting_dates
left join revenues_per_period
on reporting_dates.reporting_period = revenues_per_period.reporting_period
and reporting_dates.reporting_date = revenues_per_period.reporting_date
where reporting_dates.reporting_period = 'Year'
)

select * from final

