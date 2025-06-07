create table employee(
    employee_id varchar(50) primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null
);

create table mentor(
    mentor_id varchar(50) primary key,
    xp_level int default 0,
    amount_of_students int default 0,
    supervisor varchar(50),
    foreign key (supervisor) references mentor(mentor_id) on delete set null,
    foreign key (mentor_id) references employee(employee_id) on delete cascade
);

create table tutor(
    tutor_id varchar(50) primary key ,
    language_speciality varchar(50) not null,
    years_of_experience int default 0,
    foreign key (tutor_id) references employee(employee_id) on delete cascade
);

create table student(
    student_id varchar(50) primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(50) not null,
    age int not null,
    mentor varchar(50),
    foreign key (mentor) references mentor(mentor_id) on delete set null
);

create table course(
    course_id varchar(50) primary key,
    language varchar(50) not null,
    title varchar(50) not null,
    level varchar(50) not null,
    tutor varchar(50) not null,
    foreign key (tutor) references tutor(tutor_id) on delete restrict
);

create table student_group(
    student_group_id varchar(50),
    course_id varchar(50),
    age_category varchar(50) not null,
    amount_of_participants int default 0,
    max_participants int not null,

    primary key (student_group_id, course_id),
    foreign key (course_id) references course(course_id) on delete cascade
);

create table assignment(
    assignment_id varchar(50) primary key,
    date_issued datetime not null,
    date_due datetime not null,
    submission_date datetime,
    from_student varchar(50) not null,
    foreign key (from_student) references student(student_id) on delete cascade
);

create table checked_assignments(
    grade int default 0,
    assignment_id varchar(50) primary key,
    mentor_id varchar(50),
    checked_date datetime,
    foreign key (assignment_id) references assignment(assignment_id) on delete cascade,
    foreign key (mentor_id) references mentor(mentor_id) on delete set null
);

create table group_membership(
    student_id varchar(50) not null,
    student_group_id varchar(50) not null,
    course_id varchar(50) not null,
    primary key (student_group_id, course_id, student_id),
    foreign key (student_id) references student(student_id) on delete cascade,
    foreign key (student_group_id, course_id) references student_group(student_group_id, course_id) on delete cascade
);



-- CREATE TRIGGER increment_participants
-- AFTER INSERT ON group_membership
-- FOR EACH ROW
-- BEGIN
--     UPDATE student_group
--     SET amount_of_participants = amount_of_participants + 1
--     WHERE student_group_id = NEW.student_group_id
--       AND course_id = NEW.course_id;
-- END;

-- CREATE TRIGGER decrement_participants
-- AFTER DELETE ON group_membership
-- FOR EACH ROW
-- UPDATE student_group
-- SET amount_of_participants = amount_of_participants - 1
-- WHERE student_group_id = OLD.student_group_id AND course_id = OLD.course_id;

commit;

