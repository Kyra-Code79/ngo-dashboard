-- Enable RLS
alter table datasets enable row level security;

create policy "Users can view their own datasets" 
on datasets for select
using (auth.uid() = uploaded_by);
