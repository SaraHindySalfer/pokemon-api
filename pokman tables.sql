use sql_intro;
drop table type;
drop table OwnedBy;
drop table pokemon;
drop table trainer;

create table pokemon(
    id int primary key,
    name varchar(20),
    weight int,
    height int
);

create table trainer(
    name varchar(20) primary key,
    town varchar(20)
);

create table OwnedBy(
    pokemon_id int ,
    trainer_name varchar(20),
    primary key(pokemon_id,trainer_name),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(trainer_name) REFERENCES trainer(name)
);

create table type(
    pokemon_type varchar(20),
    pokemon_id int,
    primary key (pokemon_id,pokemon_type),
    FOREIGN key (pokemon_id) REFERENCES pokemon(id)
);
