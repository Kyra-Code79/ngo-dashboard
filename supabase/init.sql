-- Supabase Initiate
create table datasets (
  id uuid primary key default uuid_generate_v4(),
  name text,
  description text,
  status text,
  uploaded_by uuid references auth.users(id),
  created_at timestamp default now()
);
