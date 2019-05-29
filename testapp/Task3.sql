create table t1 ( 
    ID int primary key not null,
    Name char(20) not null,
    Surname char(20) not null,
    "Salary/year" int not null
);

create table t2 (
    ID int primary key not null,
    Month char(20) not null,
    Taxes int not null,
    EmployeeID int not null
);

create table t3 (
    ID int primary key not null,
    InternalNumber int not null,
    Position char(20) not null,
    EmployeeID int not null
);


insert into t1
    values (1, "John", "Terrible", 11000)
    UNION all
    values (2, "Maggie", "Woodstock", 15000)
    UNION all
    values (3, "Joel", "Muegos", 22000)
    UNION all
    values (4, "Jeroen", "van Kapf", 44000);
    
insert into t2
    values (1, "01.01.15", "250", 1)
    UNION all
    values (2, "01.02.15", "267", 1)
    UNION all
    values (3, "01.01.15", "300", 2)
    UNION all
    values (4, "01.02.15", "350", 2)
    UNION all
    values (5, "01.01.15", "245", 3)
    UNION all
    values (6, "01.02.15", "356", 3)
    UNION all
    values (7, "01.01.15", "246", 4)
    UNION all
    values (8, "01.02.15", "356", 4)
    UNION all
    values (9, "01.03.15", "412", 3);

insert into t3
    values (1, "32894", "Manager", 1)
    UNION all
    values (2, "23409", "Top Manager", 2)
    UNION all
    values (3, "23908", "CEO", 3)
    UNION all
    values (4, "128", "Board Chairman", 4);

select InternalNumberr as InternalNumber, "Name/Surname", Positionn as Position, "Salary/month", Taxes as Tax, Month from
(
    select t3.EmployeeID as EmployeeIDD, InternalNumber as InternalNumberr, Name || ' ' || Surname as "Name/Surname", Position as Positionn, "Salary/year"/12 as "Salary/month" from t1 
        left join t3 on t1.ID = t3.ID
)
    left join t2 on t2.EmployeeID = EmployeeIDD;