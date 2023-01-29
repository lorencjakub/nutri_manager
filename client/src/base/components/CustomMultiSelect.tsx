import { FC, useEffect, useState } from "react"
import {
    Checkbox,
    InputLabel,
    ListItemIcon,
    ListItemText,
    MenuItem,
    FormControl,
    Select,
    Box,
    Chip
} from "@mui/material"
import { Cancel as CancelIcon } from "@mui/icons-material"
import { useFormData } from "../../app/Providers/FormData"
import { TFormField } from "../utils/types"
import { useIntl } from "react-intl"


const ITEM_HEIGHT = 48
const ITEM_PADDING_TOP = 8
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250
        }
    },
    getContentAnchorEl: null,
    anchorOrigin: {
        vertical: "bottom",
        horizontal: "center"
    },
    transformOrigin: {
        vertical: "top",
        horizontal: "center"
    },
    variant: "menu"
}

const options = [
    "Option 1",
    "Option 2",
    "Option 3"
]

export { MenuProps, options }

const CustomMultiSelect: FC<{ inputName: string, data: TFormField }> = ({ inputName, data }) => {
    const { formData = {}, setFormData } = useFormData()
    const [ selected, setSelected ] = useState<string[]>([])
    const isAllSelected = options.length > 0 && selected.length === options.length
    const intl = useIntl()

    const handleChange = (event: any) => {
        const value = event.target.value
        if (value[value.length - 1] === "all") {
            setSelected(selected.length === options.length ? [] : options);
            return
        }
        setSelected(value)
    }

    const handleDeleteOption = (value: string) => {
        var newSelectOptions = selected.filter((s) => s != value)
        setSelected(newSelectOptions)
    }

    useEffect(() => {
        if (setFormData) {
            setFormData({ ...formData, [inputName]: selected as string[] })}
    }, [selected])

    return (
        <FormControl
            key={`${inputName}_multiselect.formcontrol`}
        >
            <InputLabel
                key={`${inputName}_multiselect.label`}
                id={`${inputName}_multiselect.label`}
            >
                {data.label}
            </InputLabel>
            <Select
                label={data.label}
                labelId={`${inputName}_multiselect.label`}
                key={`${inputName}_multiselect.input`}
                name={inputName}
                multiple
                value={selected}
                onChange={handleChange}
                renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                            <Chip
                                key={`${inputName}_multiselect.options.${value}`}
                                label={value}
                                clickable
                                deleteIcon={
                                    <CancelIcon
                                        onMouseDown={(event) => event.stopPropagation()}
                                    />
                                }
                                onDelete={() => handleDeleteOption(value)}
                            />
                        ))}
                    </Box>
                )}
                MenuProps={MenuProps as any}
                displayEmpty={true}
                sx={{
                    maxWidth: 250
                }}
            >
                <MenuItem value="all">
                    <ListItemIcon>
                        <Checkbox
                            checked={isAllSelected}
                            indeterminate={selected.length > 0 && selected.length < options.length}
                        />
                    </ListItemIcon>
                    <ListItemText primary={intl.formatMessage({ id: "multiselect.options.select_all", defaultMessage: "Select All" })} />
                </MenuItem>
                {options.map((option) => (
                    <MenuItem key={option} value={option}>
                        <ListItemIcon>
                            <Checkbox checked={selected.indexOf(option) > -1} />
                        </ListItemIcon>
                        <ListItemText primary={option} />
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    )
}

export default CustomMultiSelect