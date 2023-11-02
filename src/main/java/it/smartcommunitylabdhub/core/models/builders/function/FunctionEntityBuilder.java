package it.smartcommunitylabdhub.core.models.builders.function;

import it.smartcommunitylabdhub.core.models.base.JacksonMapper;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.stereotype.Component;

@Component
public class FunctionEntityBuilder extends JacksonMapper {

    /**
     * Build a function from a functionDTO and store extra values as a cbor
     *
     * @param functionDTO the functionDTO that need to be stored
     * @return Function
     */
    public Function build(FunctionDTO functionDTO) {

        // Retrieve Spec
        FunctionBaseSpec spec = mapper.convertValue(functionDTO.getSpec(), FunctionBaseSpec.class);

        return EntityFactory.combine(
                ConversionUtils.convert(functionDTO, "function"), functionDTO,
                builder -> builder
                        .with(f -> f.setMetadata(
                                ConversionUtils.convert(functionDTO
                                                .getMetadata(),
                                        "metadata")))
                        .with(f -> f.setExtra(
                                ConversionUtils.convert(functionDTO
                                                .getExtra(),
                                        "cbor")))
                        .with(f -> f.setSpec(
                                ConversionUtils.convert(spec.toMap(),
                                        "cbor"))));
    }

    /**
     * Update a function if element is not passed it override causing empty field
     *
     * @param function the function to update
     * @return Function
     */
    public Function update(Function function, FunctionDTO functionDTO) {

        // Retrieve object spec
        FunctionBaseSpec spec = mapper.convertValue(functionDTO.getSpec(), FunctionBaseSpec.class);

        return EntityFactory.combine(
                function, functionDTO, builder -> builder
                        .with(f -> f.setKind(functionDTO.getKind()))
                        .with(f -> f.setProject(functionDTO.getProject()))
                        .with(f -> f.setName(functionDTO.getName()))
                        .with(f -> f.setState(functionDTO.getState() == null
                                ? State.CREATED
                                : State.valueOf(functionDTO
                                .getState())))
                        .with(f -> f.setMetadata(
                                ConversionUtils.convert(functionDTO
                                                .getMetadata(),
                                        "metadata")))

                        .with(f -> f.setExtra(
                                ConversionUtils.convert(functionDTO
                                                .getExtra(),

                                        "cbor")))
                        .with(f -> f.setSpec(
                                ConversionUtils.convert(spec.toMap(),
                                        "cbor")))
                        .with(f -> f.setEmbedded(
                                functionDTO.getEmbedded())));
    }
}
