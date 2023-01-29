import React, { FC, useState, useEffect } from "react"
import {
    FormControlLabel,
    Button,
    TextField,
    Checkbox,
    Select,
    Paper,
    Box,
    Grid,
    Typography,
    Slider,
    Input,
    Tooltip,
    SliderValueLabelProps
} from "@mui/material"
import { useFormData } from "../Providers/FormData"
import {
    TFormField,
    IFormData,
    IFormFields
} from "../../base/utils/types"
import CustomMultiSelect from "../../base/components/CustomMultiSelect"


function ValueLabelComponent(props: SliderValueLabelProps) {
    const { children, value } = props;
  
    return (
        <Tooltip enterTouchDelay={0} placement="top" title={value}>
            {children}
        </Tooltip>
    )
  }

const Form: FC<{ fields: IFormFields}> = ({ fields = {} }) => {
    const { formData = {}, setFormData } = useFormData()

    useEffect(() => {
        var initialValues: IFormData = {}
        Object.entries(fields).forEach(([fieldName, fieldData]) => { initialValues[fieldName] = fieldData.defaultvalue })
        if (setFormData) setFormData(initialValues)
    }, [])

    const handleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (setFormData) setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleSliderChange = (inputName: string, value: number) => {
        if (setFormData) setFormData({ ...formData, [inputName]: value})
    }

    const handleBindedSliderChange = (inputName: string, value: number) => {
        var newData = { ...formData }
        var sumOfOtherSliders = 0
        var slidersNames = Object.keys(newData).filter((name) => {
            if (fields[name].type == "binded_slider" && (name != inputName)) {
                sumOfOtherSliders += Number(newData[name]) || 0
                return name
            }
        })
        const onePiece = ((100 - value) == 0) ? 0 : (100 - value) / sumOfOtherSliders

        slidersNames.forEach((name) => {
            if (newData[name]) {
                newData[name] = Math.round(onePiece * Number(newData[name]))
            }
        })

        if (setFormData) setFormData({ ...newData, [inputName]: value})
    }

    const handleChangeCheckboxField = (inputName: string, checked: boolean) => {
        if (setFormData) setFormData({ ...formData, [inputName]: checked })
    }

    return (
        <Paper
            elevation={1}
            sx={{
                
            }}
        >
            <Grid
                container
                direction="column"
                sx={{
                    p: 2
                }}
            >
                {Object.entries(fields).map(([fieldName, fieldData]: [string, TFormField]) => {
                    if (fieldData.type == "checkbox") {
                        return (
                            <Grid
                                item
                                xs={12}
                                sx={{
                                    my: 1
                                }}
                            >
                                <FormControlLabel
                                    label={fieldData.label}
                                    control={
                                        <Checkbox
                                            checked={(formData[fieldName] == undefined) ? Boolean(fieldData.defaultvalue) : Boolean(formData[fieldName])}
                                            onChange={(e, checked) => handleChangeCheckboxField(fieldName, checked)}
                                            required={fieldData.required}
                                            disabled={fieldData.disabled}
                                        />
                                    }
                                />
                            </Grid>
                        )
                    } else if (fieldData.type && fieldData.type.includes("slider")) {
                        return (
                            <Box
                                sx={{
                                    width: 250,
                                    my: 1
                                }}
                            >
                                <Typography id="input-slider" gutterBottom>
                                    {fieldData.label}
                                </Typography>
                                <Grid container spacing={2} alignItems="center">
                                    <Grid item xs>
                                        <Slider
                                            value={(Number(formData[fieldName]) === 0) ? 0 : Number(formData[fieldName]) || Number(fieldData.defaultvalue)}
                                            onChange={(event: Event, value: number | number[], activeThumb: number) => {
                                                (fieldData.type == "binded_slider") ?
                                                handleBindedSliderChange(fieldName, Array.isArray(value) ? value[0] : value)
                                                :
                                                handleSliderChange(fieldName, Array.isArray(value) ? value[0] : value)
                                            }}
                                            aria-labelledby="input-slider"
                                            valueLabelDisplay="auto"
                                            slots={{
                                                valueLabel: ValueLabelComponent,
                                            }}
                                            aria-label="custom thumb label"
                                            defaultValue={Number(fieldData.defaultvalue)}
                                            min={Number(fieldData.min) || 0}
                                            max={Number(fieldData.max) || 100}
                                        />
                                    </Grid>
                                </Grid>
                            </Box>
                        )
                    } else if (fieldData.type == "multiselect") {
                        return <CustomMultiSelect inputName={fieldName} data={fieldData} />
                    } else {
                        return (
                            <Grid
                                item
                                xs={12}
                                sx={{
                                    my: 1
                                }}
                            >
                                <TextField
                                    label={fieldData.label}
                                    value={formData[fieldName] || fieldData.defaultvalue}
                                    type={fieldData.type || "text"}
                                    onChange={handleChangeInput}
                                    required={fieldData.required}
                                    InputProps={{
                                        disabled: fieldData.disabled
                                    }}
                                />
                            </Grid>
                        )
                    }
                })}
            </Grid>
        </Paper>
    )
}

export default Form