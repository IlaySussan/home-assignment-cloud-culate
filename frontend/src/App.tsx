import { useState } from 'react';
import ItemList from './components/ItemList';
import { deleteAllScrapedArchitectures, fetchItems, scrapeUrl } from './api';
import { Box, TextField, Button, CircularProgress, Typography, Container } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function App() {
  const [url, setUrl] = useState('');
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFetchItems = async () => {
    try {
      const fetchedItems = await fetchItems();
      setItems(fetchedItems);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const handleScrapeUrl = async (url: string) => {
    setLoading(true);
    setUrl('');
    try {
      await scrapeUrl(url);
      await handleFetchItems();
    } catch (error) {
      console.error('Error scraping URL:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAll = async () => {
    setLoading(true);
    try {
      await deleteAllScrapedArchitectures();
      setItems([]);
    } catch (error) {
      console.error('Error deleting all scraped architectures:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box
      sx={{
        position: 'relative',
        minHeight: '100vh',
        width: '100vw',
        overflowX: 'hidden',
        overflowY: 'auto',
        padding: '2rem',
        boxSizing: 'border-box',
      }}
    >
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          zIndex: -2,
        }}
      />
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '200%',
          height: '200%',
          background:
            'radial-gradient(circle at 20% 20%, rgba(255,255,255,0.05) 0%, transparent 60%)',
          animation: 'move 20s linear infinite',
          zIndex: -1,
        }}
      />
      <div className="app-container">
        <Typography variant="h4" sx={{ color: 'white', mb: 2 }}>
          Amazon AWS Architectures Web Scraper
        </Typography>
        
        <div
          className="input-section"
          style={{
            display: 'flex',
            gap: '1rem',
            flexWrap: 'wrap',
            alignItems: 'center',
            marginBottom: '1.5rem',
            justifyContent: 'center',
          }}
        >{!loading ? (
          <><TextField
              id="standard-basic"
              label="Enter URL"
              variant="standard"
              value={url}
              color='primary'
               sx={{
                width: '30vw',
                input: {
                  color: 'white',
                },
                label: {
                  color: 'white',
                },
                '& label.Mui-focused': {
                  color: 'white',
                },
                '& .MuiInput-underline:before': {
                  borderBottomColor: 'primary.main',
                },
                '& .MuiInput-underline:hover:before': {
                  borderBottomColor: 'primary.main',
                },
                '& .MuiInput-underline:after': {
                  borderBottomColor: 'primary.main',
                },
              }}
              onChange={(e) => setUrl(e.target.value)} /><Button
                variant="contained"
                endIcon={<SendIcon />}
                onClick={() => handleScrapeUrl(url)}
                disabled={loading}
              >
                Scrape URL
              </Button><Button variant="contained" onClick={handleFetchItems} disabled={loading}>
                Display Scraped Architectures
              </Button>
              <Button variant="contained" onClick={handleDeleteAll} disabled={loading}>
                Delete all previously scraped architectures
              </Button>
                      <Container
        sx={{
          height: '60vh',
          overflowY: 'auto',
          background: 'rgba(255,255,255,0.05)',
          borderRadius: 2,
          scrollbarWidth: 'thin',
          scrollbarColor: '#5a98dbff #eef0f3ff',
        }}
    >
      <ItemList items={items} />
    </Container></>) : (
           <CircularProgress color="primary" size={200} />)}
        </div>

      </div>

      <style>
        {`
          @keyframes move {
            0% { transform: rotate(0deg) translateX(0); }
            100% { transform: rotate(360deg) translateX(0); }
          }
        `}
      </style>
    </Box>
  );
}

export default App;
