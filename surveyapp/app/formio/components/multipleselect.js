const {
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Chip,
    Box,
    OutlinedInput,
} = MaterialUI;

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};


function MultipleSelectChip({ options, onChange, selectedValue, getLabel }) {
    const handleChange = (event) => {
        const {
            target: { value },
        } = event;
        onChange(typeof value === 'string' ? value.split(',') : value)
    };

    return (
        <div>
            <InputLabel>Languages</InputLabel>
            <Select
                labelId="demo-multiple-chip-label"
                id="demo-multiple-chip"
                multiple
                value={selectedValue}
                onChange={handleChange}
                fullWidth
                input={<OutlinedInput id="select-multiple-chip" label="Languages" />}
                renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                            <Chip key={`selected-languages-${value}-chip`} label={getLabel(value)} />
                        ))}
                    </Box>
                )}
                MenuProps={MenuProps}
            >
                {options.map(({ key, value, label }) => (
                    <MenuItem
                        key={`selected-languages-${value}-option`} 
                        value={value}
                    >
                        {label}
                    </MenuItem>
                ))}
            </Select>
        </div>
    );
}