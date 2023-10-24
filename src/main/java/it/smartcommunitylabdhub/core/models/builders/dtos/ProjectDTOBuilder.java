package it.smartcommunitylabdhub.core.models.builders.dtos;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.artifact.Artifact;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItem;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.project.Project;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectDTO;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectMetadata;
import it.smartcommunitylabdhub.core.models.entities.workflow.Workflow;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class ProjectDTOBuilder {

        @Autowired
        ArtifactDTOBuilder artifactDTOBuilder;

        @Autowired
        FunctionDTOBuilder functionDTOBuilder;

        @Autowired
        WorkflowDTOBuilder workflowDTOBuilder;

        @Autowired
        DataItemDTOBuilder dataItemDTOBuilder;

        @Autowired
        MetadataConverter<ProjectMetadata> metadataConverter;

        public ProjectDTO build(
                        Project project,
                        List<Artifact> artifacts,
                        List<Function> functions,
                        List<Workflow> workflows,
                        List<DataItem> dataItems,
                        boolean embeddable) {

                return EntityFactory.create(ProjectDTO::new, project, builder -> builder
                                .with(dto -> dto.setId(project.getId()))
                                .with(dto -> dto.setName(project.getName()))
                                .with(dto -> dto.setDescription(project.getDescription()))
                                .with(dto -> dto.setSource(project.getSource()))
                                .with(dto -> dto.setState(
                                                project.getState() == null ? State.CREATED.name()
                                                                : project.getState().name()))
                                .with(dto -> dto.setExtra(ConversionUtils.reverse(
                                                project.getExtra(),
                                                "cbor")))
                                .with(dto -> dto.setSpec(ConversionUtils.reverse(
                                                project.getSpec(),
                                                "cbor")))
                                .with(dto -> dto.setMetadata(Optional
                                                .ofNullable(
                                                                metadataConverter.reverseByClass(
                                                                                project.getMetadata(),
                                                                                ProjectMetadata.class))
                                                .orElseGet(ProjectMetadata::new)))
                                .with(dto -> dto.getSpec().put("functions",
                                                functions.stream()
                                                                .map(f -> functionDTOBuilder.build(
                                                                                f, embeddable))
                                                                .collect(Collectors.toList())))
                                .with(dto -> dto.getSpec().put("artifacts",
                                                artifacts.stream()
                                                                .map(a -> artifactDTOBuilder.build(
                                                                                a,
                                                                                embeddable))
                                                                .collect(Collectors.toList())))
                                .with(dto -> dto.getSpec().put("workflows",
                                                workflows.stream()
                                                                .map(w -> workflowDTOBuilder.build(
                                                                                w, embeddable))
                                                                .collect(Collectors.toList())))
                                .with(dto -> dto.getSpec().put("dataitems",
                                                dataItems.stream()
                                                                .map(d -> dataItemDTOBuilder.build(
                                                                                d, embeddable))
                                                                .collect(Collectors.toList())))
                                .with(dto -> dto.setCreated(project.getCreated()))
                                .with(dto -> dto.setUpdated(project.getUpdated()))

                );
        }
}
