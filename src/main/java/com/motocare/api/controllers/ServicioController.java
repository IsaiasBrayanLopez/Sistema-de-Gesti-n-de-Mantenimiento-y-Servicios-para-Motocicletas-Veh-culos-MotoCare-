package com.motocare.api.controllers;

import com.motocare.api.models.RegistroServicio;
import com.motocare.api.repositories.RegistroServicioRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/servicios")
@CrossOrigin(origins = "*")
public class ServicioController {

    private final RegistroServicioRepository repository;

    public ServicioController(RegistroServicioRepository repository) {
        this.repository = repository;
    }

    /** Lista todos los servicios asociados a un usuario ordenados por fecha descendente. */
    @GetMapping("/usuario/{idUsuario}")
    public List<RegistroServicio> listarPorUsuario(@PathVariable Integer idUsuario) {
        return repository.findByIdUsuarioOrderByFechaServicioDesc(idUsuario);
    }

    /** Crea un nuevo registro de mantenimiento. */
    @PostMapping
    public ResponseEntity<RegistroServicio> crear(@RequestBody RegistroServicio servicio) {
        RegistroServicio guardado = repository.save(servicio);
        return ResponseEntity.status(HttpStatus.CREATED).body(guardado);
    }

    /** Actualiza los campos de un servicio existente por su identificador. */
    @PutMapping("/{id}")
    public ResponseEntity<RegistroServicio> actualizar(
            @PathVariable Integer id,
            @RequestBody RegistroServicio datos) {
        return repository.findById(id)
                .map(existente -> {
                    existente.setTipoServicio(datos.getTipoServicio());
                    existente.setKilometraje(datos.getKilometraje());
                    existente.setCosto(datos.getCosto());
                    existente.setFechaServicio(datos.getFechaServicio());
                    existente.setProximoKilometraje(datos.getProximoKilometraje());
                    existente.setEstado(datos.getEstado());
                    existente.setObservaciones(datos.getObservaciones());
                    return ResponseEntity.ok(repository.save(existente));
                })
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    /** Elimina fisicamente un registro de servicio. */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Integer id) {
        if (!repository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        repository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
