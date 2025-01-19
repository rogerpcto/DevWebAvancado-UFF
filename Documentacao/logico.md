Usuario (<u>id</u>, email (unique), nome, senha, perfil)

Review (<u>id_usuario</u>, <u>id_midia</u>, comentario, nota)
- id_usuario referencia Usuario(id)
- id_midia referencia Midia(id)

Diretor (<u>id</u>, nome)

Midia (<u>id</u>, titulo, nota, data_de_lancamento, genero, id_diretor)
- id_diretor referencia Diretor(id)

Filme (<u>id_midia</u>, duracao)

Temporada (<u>id_midia</u>, <u>numero</u>)
- id_midia referencia Midia(id)

Episodio (<u>id_midia</u>, duracao, {<u>id_serie</u>, <u>numero_temporada</u>}, <u>numero_episodio</u>)
- id_midia referencia Midia(id)
- {<u>id_serie</u>, <u>numero_temporada</u>} referencia Temporada
