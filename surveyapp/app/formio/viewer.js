const {
  Container,
  ThemeProvider,
  CssBaseline
} = MaterialUI;


function App() {
  
  return (
    <Container maxWidth={false}>
      <FormioForm
        name={datafrombackend.name}
        schema={datafrombackend.formSchema}
        translations={datafrombackend.translations}
      />
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