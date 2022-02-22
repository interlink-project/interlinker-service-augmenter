const {
    CssBaseline,
    ThemeProvider,
    Container,
    InputLabel,
    TextField,
    Button,
    Box,
    Avatar,
    Typography
} = MaterialUI;


function App() {
    const [title, setTitle] = React.useState("");
    const [description, setDescription] = React.useState("");
    const [error, setError] = React.useState("");
    const [created, setCreated] = React.useState(false);
    const inIframe = window.location !== window.parent.location

    React.useEffect(() => {
        if (inIframe) {
            window.parent.postMessage({
                'code': 'initialized',
            }, origin);
        }
    }, [])

    const sendMessage = (code, data) => {
        const dataToSend = {
          id: data._id
        }
        if (inIframe) {
          window.parent.postMessage({
            'code': code,
            'message': dataToSend
          }, origin);
        } else {
          setCreated(dataToSend)
        }
      }
    

    const submit = () => {
        if (!title) {
            setError("title")
            return
        }
        if (!description) {
            setError("description")
            return
        }
        service.create({ title, description }).then(response => {
            console.log("RESPONSE CONFIRM", response.data);
            sendMessage("asset_created", response.data);
            
            var { domain } = jQuery('#data').data();
            servicepediaUrl=domain.SERVICEPEDIA_URL;

            window.location.replace(`${servicepediaUrl}/saveSurvey?assetId=${response.data['_id']}&surveyTitle=${response.data['title']}&surveyDesc=${response.data['description']}`);
            
            
        })
    }
    return (
        <Container maxWidth="md">
            {created ?
                (<Box
                    sx={{
                        maxWidth: 450,
                        mx: 'auto',
                        alignItems: "center"
                    }}
                >
                    <Box
                        sx={{
                            display: 'flex',
                            justifyContent: 'center',
                        }}
                    >
                        <Avatar
                            src=""
                        />
                    </Box>
                    <Box sx={{ mt: 2 }}>
                        <Typography
                            align='center'
                            color='textPrimary'
                            variant='h3'
                        >
                            Asset created!
                        </Typography>
                    </Box>
                    <Box sx={{ mt: 2 }}>
                        <Typography
                            align='center'
                            color='textSecondary'
                            variant='subtitle1'
                        >
                            The asset is now accessible for this task.
                        </Typography>
                    </Box>
                    <Box
                        sx={{
                            display: 'flex',
                            justifyContent: 'center',
                            mt: 2,
                        }}
                    >
                        <Button
                            color='primary'
                            variant='contained'
                            href={`${basepath}/assets/${created.id}/view`}
                        >
                            Open asset
                        </Button>
                    </Box>
                </Box>)
                : (
                    <React.Fragment>
                        <InputLabel>Title</InputLabel>

                        <TextField error={error === "title"} helperText={title === "" && "Required"} variant="outlined" value={title} fullWidth onChange={(e) => setTitle(e.target.value)} />
                        <InputLabel sx={{ mt: 2 }}>Description</InputLabel>
                        <TextField error={error === "description"} helperText={description === "" && "Required"} variant="outlined" value={description} fullWidth onChange={(e) => setDescription(e.target.value)} />
                        <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={() => submit()}>Create</Button>
                    </React.Fragment>
                )}
        </Container>
    );
}

ReactDOM.render(
    <ThemeProvider theme={theme}>
        {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
        <CssBaseline />
        <App />
    </ThemeProvider>,
    document.querySelector('#root'),
);