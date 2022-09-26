------------------------------------------------------------------------------------------
-- Analysis of Receipt Age (dos_to_placed) vs Processing Time (placed_to_latest_payment)
------------------------------------------------------------------------------------------
select * from public.tpl_apollo_invoice_details where duplicate_payment = false;
select * from public.tpl_athena_invoice_details where duplicate_payment = false AND voided = false;
select * from public.tpl_mva_invoice_details where duplicate_payment = false AND voided = false;
select * from public.tpl_thr_invoice_details where voided = false

--explain analyze
with cte1 as (
	select pat_acct, max(charges) charges, case when sum(payment) > max(charges) then max(charges) else sum(payment) end as payment, max(payment_date) last_payment_date
	from (
        select pat_acct, round(charges) charges, round(total_payment) payment, payment_date
        from tpl_apollo_invoice_details where duplicate_acct = false and duplicate_payment = false
        ) foo1
	group by pat_acct
)
, cte2 as (
	select pat_acct, max(charges) charges, case when sum(payment) > max(charges) then max(charges) else sum(payment) end payment, max(payment_date) last_payment_date 
	from (
	    select pat_acct, round(charges) charges, round(total_payment) payment, payment_date
	    from tpl_athena_invoice_details where duplicate_payment = false AND voided = false
	    ) foo1
	group by pat_acct
)
, cte3 as (
	select pat_acct, max(charges) charges, case when sum(payment) > max(charges) then max(charges) else sum(payment) end payment, max(payment_date) last_payment_date 
	from (
	    select pat_acct, round(charges) charges, round(trans_amt) payment, trans_date payment_date
        from tpl_mva_invoice_details where duplicate_payment = false AND voided = false
        ) foo1
	group by pat_acct
)
, cte4 as (
	select pat_acct, max(charges) charges, case when sum(payment) > max(charges) then max(charges) else sum(payment) end payment, max(payment_date) last_payment_date
	from (
	    select pat_acct, round(charges) charges, round(trans_amt) payment, trans_date payment_date
        from tpl_thr_invoice_details where voided = false
        ) foo1
	group by pat_acct)
, cte5 as (
	select
		min(cust_id) cust_id
		, pat_acct
		, insurance_name
		, case when string_agg(distinct status::text, '; ') in ('B; PC', 'E; PB', 'B; PB', 'B; W', 'B; E') 
			then 'B'
		else 
			case when string_agg(distinct status::text, '; ')in ('E; PC', 'B; E; PC') 
				then 'PC'
			else
				case when string_agg(distinct status::text, '; ') = 'PB; W'  
					then 'PB'
				else 
					string_agg(distinct status::text, '; ') end end end pre_billing_claim_status
		, round(max(charges), 0) charges
	from (
		select
			foo2.cust_id
			, foo2.pat_acct
			, foo2.insurance_name
			, foo2.status
			, foo2.charges
		from (
			select 
				min(cust_id)
				, pat_acct
				, insurance_name
				, max(created_at) created_at
			from 
				tpl_pre_billing_records
			group by
				pat_acct
				, insurance_name) foo1
			left join (
				select cust_id, pat_acct, insurance_name, status, charges, created_at from tpl_pre_billing_records) foo2 on
				foo1.pat_acct = foo2.pat_acct and foo1.insurance_name = foo2.insurance_name and foo1.created_at = foo2.created_at
			) foo3
			group by 
				pat_acct
				, insurance_name)
, cte6 as (
	select 
		pat_acct
		, max(dos_date) dos_date
		, min(placed_date) placed_date
		from (
			select 
				pat_acct
				, greatest(admission_date, discharge_date) dos_date
				, created_at::date placed_date
			from tpl_client_raw_bills) foo1
			group by pat_acct)
, cte7 as (
	select 
		pat_acct
		, max(dos_date) dos_date
		, min(placed_date) placed_date
		from (
			select 
				pat_acct
				, greatest(admit_date_or_service_date, discharge_date)::date dos_date
				, created_at::date placed_date
			from tpl_raw_bills) foo1
			group by pat_acct)
-->
------------------------------------------------------------------------------------------------------------------------
-- All accounts records
------------------------------------------------------------------------------------------------------------------------
select * from (
select
		tpl_cust_infos.master_id
		, initcap(tpl_cust_infos.cust_name) cust_name
		, foo1.cust_id
		, foo1.pat_acct
		, foo1.pre_billing_claim_status_list
		, foo2.dos_date
		, foo2.placed_date
		, foo2.days_dos_to_placed
		, foo1.charge
		, case when foo3.payment = 0 then null else foo3.payment end payment
		, foo3.last_payment_date
		, foo3.last_payment_date - foo2.placed_date days_placed_to_last_payment
	from (
		select 
			min(cust_id) cust_id
			, pat_acct
			, string_agg(distinct pre_billing_claim_status, '; ') pre_billing_claim_status_list
			, max(charges) charge
		from 
			cte5
		group by 
			pat_acct
		having 
			string_agg(distinct pre_billing_claim_status, '; ') ~* 'B'
			and string_agg(distinct pre_billing_claim_status, '; ') not in ('E; PB', 'PB', 'PB; PC', 'PB; W')) foo1
	left join (
		select 
			coalesce(cte6.pat_acct, cte7.pat_acct) pat_acct
			, greatest(cte6.dos_date, cte7.dos_date) dos_date
			, least(cte6.placed_date, cte7.placed_date) placed_date
			, least(cte6.placed_date, cte7.placed_date) - greatest(cte6.dos_date, cte7.dos_date) days_dos_to_placed
		from
			cte6 full join cte7 on
			cte6.pat_acct = cte7.pat_acct) foo2 on
		foo1.pat_acct = foo2.pat_acct
	left join (				
		select pat_acct, payment, last_payment_date from cte1
		union all 
		select pat_acct, payment, last_payment_date from cte2
		union all
		select pat_acct, payment, last_payment_date from cte3
		union all 
		select pat_acct, payment, last_payment_date from cte4) foo3 on
		foo1.pat_acct = foo3.pat_acct
	left join tpl_cust_infos on
		foo1.cust_id = tpl_cust_infos.cust_id
		) foo4
where
    (days_dos_to_placed is not null and days_dos_to_placed::text != '')
    and (days_placed_to_last_payment > 0 or days_placed_to_last_payment is null or days_placed_to_last_payment::text = '')
    and (payment > 0 or payment is null or payment::text = '')
------------------------------------------------------------------------------------------------------------------------
-- Group by Age by Yield
------------------------------------------------------------------------------------------------------------------------
select
	days_dos_to_placed
	, count(charge) billed_accts
	, count(payment) paid_accts
	, round(count(payment)::numeric / count(charge), 2) volumes_yield
	, sum(charge) billed_dollars
	, sum(payment) paid_dollars
	, case when round(sum(payment) / sum(charge), 2) is null then 0 else round(sum(payment) / sum(charge), 2) end dollars_yield
from (
select
		foo1.pat_acct
		, foo1.pre_billing_claim_status_list
		, foo2.dos_date
		, foo2.placed_date
		, foo2.days_dos_to_placed
		, foo1.charge
		, case when foo3.payment = 0 then null else foo3.payment end payment
		, foo3.last_payment_date
		, foo3.last_payment_date - foo2.placed_date days_placed_to_last_payment
	from (
		select
			pat_acct
			, string_agg(distinct pre_billing_claim_status, '; ') pre_billing_claim_status_list
			, max(charges) charge
		from
			cte5
		group by
			pat_acct
		having
			string_agg(distinct pre_billing_claim_status, '; ') ~* 'B'
			and string_agg(distinct pre_billing_claim_status, '; ') not in ('E; PB', 'PB', 'PB; PC', 'PB; W')) foo1
	left join (
		select
			coalesce(cte6.pat_acct, cte7.pat_acct) pat_acct
			, greatest(cte6.dos_date, cte7.dos_date) dos_date
			, least(cte6.placed_date, cte7.placed_date) placed_date
			, least(cte6.placed_date, cte7.placed_date) - greatest(cte6.dos_date, cte7.dos_date) days_dos_to_placed
		from
			cte6 full join cte7 on
			cte6.pat_acct = cte7.pat_acct) foo2 on
		foo1.pat_acct = foo2.pat_acct
	left join (
		select pat_acct, payment, last_payment_date from cte1
		union all
		select pat_acct, payment, last_payment_date from cte2
		union all
		select pat_acct, payment, last_payment_date from cte3
		union all
		select pat_acct, payment, last_payment_date from cte4) foo3 on
		foo1.pat_acct = foo3.pat_acct
		) foo4
where
    (days_dos_to_placed is not null and days_dos_to_placed::text != '')
    and (days_placed_to_last_payment > 0 or days_placed_to_last_payment is null or days_placed_to_last_payment::text = '')
    and (payment > 0 or payment is null or payment::text = '')
group by
    days_dos_to_placed
------------------------------------------------------------------------------------------------------------------------
-- Group by Age by Effort Proxy
------------------------------------------------------------------------------------------------------------------------
select
	days_dos_to_placed
	, count(*) valid_paid_accts
	, round(avg(days_placed_to_last_payment)) avg_days_placed_to_last_payment
	, percentile_disc(0.5) within group(order by days_placed_to_last_payment) med_days_placed_to_last_payment
from (
select
		foo1.pat_acct
		, foo1.pre_billing_claim_status_list
		, foo2.dos_date
		, foo2.placed_date
		, foo2.days_dos_to_placed
		, foo1.charge
		, case when foo3.payment = 0 then null else foo3.payment end payment
		, foo3.last_payment_date
		, foo3.last_payment_date - foo2.placed_date days_placed_to_last_payment
	from (
		select
			pat_acct
			, string_agg(distinct pre_billing_claim_status, '; ') pre_billing_claim_status_list
			, max(charges) charge
		from
			cte5
		group by
			pat_acct
		having
			string_agg(distinct pre_billing_claim_status, '; ') ~* 'B'
			and string_agg(distinct pre_billing_claim_status, '; ') not in ('E; PB', 'PB', 'PB; PC', 'PB; W')) foo1
	left join (
		select
			coalesce(cte6.pat_acct, cte7.pat_acct) pat_acct
			, greatest(cte6.dos_date, cte7.dos_date) dos_date
			, least(cte6.placed_date, cte7.placed_date) placed_date
			, least(cte6.placed_date, cte7.placed_date) - greatest(cte6.dos_date, cte7.dos_date) days_dos_to_placed
		from
			cte6 full join cte7 on
			cte6.pat_acct = cte7.pat_acct) foo2 on
		foo1.pat_acct = foo2.pat_acct
	left join (
		select pat_acct, payment, last_payment_date from cte1
		union all
		select pat_acct, payment, last_payment_date from cte2
		union all
		select pat_acct, payment, last_payment_date from cte3
		union all
		select pat_acct, payment, last_payment_date from cte4) foo3 on
		foo1.pat_acct = foo3.pat_acct
		) foo4
where
    (days_dos_to_placed is not null and days_dos_to_placed::text != '') and (days_placed_to_last_payment > 0) and (payment > 0)
group by
    days_dos_to_placed