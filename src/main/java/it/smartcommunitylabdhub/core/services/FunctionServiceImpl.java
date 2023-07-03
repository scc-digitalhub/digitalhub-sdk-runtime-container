package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.builders.dtos.FunctionDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.FunctionEntityBuilder;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.repositories.FunctionRepository;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;

@Service
public class FunctionServiceImpl implements FunctionService {

    private final FunctionRepository functionRepository;
    private final RunRepository runRepository;

    public FunctionServiceImpl(
            FunctionRepository functionRepository,
            RunRepository runRepository,
            TaskRepository taskRepository) {
        this.functionRepository = functionRepository;
        this.runRepository = runRepository;
    }

    @Override
    public List<FunctionDTO> getFunctions(Pageable pageable) {
        try {
            Page<Function> functionPage = this.functionRepository.findAll(pageable);
            return functionPage.getContent().stream().map((function) -> {
                return new FunctionDTOBuilder(function, false).build();
            }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public List<FunctionDTO> getFunctions() {
        try {
            List<Function> functions = this.functionRepository.findAll();
            return functions.stream().map((function) -> {
                return new FunctionDTOBuilder(function, false).build();
            }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO createFunction(FunctionDTO functionDTO) {
        try {
            // Build a function and store it on db
            final Function function = new FunctionEntityBuilder(functionDTO).build();
            this.functionRepository.save(function);

            // Return function DTO
            return new FunctionDTOBuilder(

                    function, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO getFunction(String uuid) {

        final Function function = functionRepository.findById(uuid).orElse(null);
        if (function == null) {
            throw new CoreException(
                    "FunctionNotFound",
                    "The function you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            return new FunctionDTOBuilder(

                    function, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO updateFunction(FunctionDTO functionDTO, String uuid) {

        if (!functionDTO.getId().equals(uuid)) {
            throw new CoreException(
                    "FunctionNotMatch",
                    "Trying to update a function with an uuid different from the one passed in the request.",
                    HttpStatus.NOT_FOUND);
        }

        final Function function = functionRepository.findById(uuid).orElse(null);
        if (function == null) {
            throw new CoreException(
                    "FunctionNotFound",
                    "The function you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {

            FunctionEntityBuilder functionBuilder = new FunctionEntityBuilder(functionDTO);

            final Function functionUpdated = functionBuilder.update(function);
            this.functionRepository.save(functionUpdated);

            return new FunctionDTOBuilder(
                    functionUpdated, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public boolean deleteFunction(String uuid) {
        try {
            if (this.functionRepository.existsById(uuid)) {
                this.functionRepository.deleteById(uuid);
                return true;
            }
            throw new CoreException(
                    "FunctionNotFound",
                    "The function you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete function",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<RunDTO> getFunctionRuns(String uuid) {
        final Function function = functionRepository.findById(uuid).orElse(null);
        if (function == null) {
            throw new CoreException(
                    "FunctionNotFound",
                    "The function you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            List<Run> runs = this.runRepository.findByTask(TaskUtils.buildTaskString(function));
            return (List<RunDTO>) ConversionUtils.reverseIterable(runs, "run", RunDTO.class);

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<FunctionDTO> getAllLatestFunctions() {
        try {

            List<Function> functionList = this.functionRepository.findAllLatestFunctions();
            return functionList
                    .stream()
                    .map((function) -> {
                        return new FunctionDTOBuilder(function, false).build();
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
