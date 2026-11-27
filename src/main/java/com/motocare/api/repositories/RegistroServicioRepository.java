package com.motocare.api.repositories;

import com.motocare.api.models.RegistroServicio;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface RegistroServicioRepository extends JpaRepository<RegistroServicio, Integer> {
    List<RegistroServicio> findByIdUsuarioOrderByFechaServicioDesc(Integer idUsuario);
}
