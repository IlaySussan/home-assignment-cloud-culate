import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

interface ComponentType {
  name: string;
  description: string;
  type: string;
}

type ParsingStatusEnum = 'Success' | 'Failed';

interface Item {
  title: string;
  description: string;
  services: string[];
  components: ComponentType[];
  use_case: string | null;
  complexity: string | null;
  estimated_cost: string | null;
  benefits: string[];
  architecture_pattern: string;
  source_url: string;
  scraped_at: Date;
  raw_title: string | null;
  parsing_status: ParsingStatusEnum;
  id: string;
}

interface ItemListProps {
  items: Item[];
}

const ItemList: React.FC<ItemListProps> = ({ items }) => (
  <Box
    className="item-list"
    sx={{
      marginTop: 2,
      display: 'flex',
      flexDirection: 'row',
      flexWrap: 'wrap',
      alignItems: 'center',
      gap: 2,
      justifyContent: 'center',
      overflowX: 'hidden',
      width: '100%',
      boxSizing: 'border-box',
      '& .MuiTypography-root': {
        fontFamily: "'Rubik', sans-serif",
      },
    }}
  >
    {items.map((item, idx) => (
      <Card
        key={idx}
        sx={{
          width: '100%',
          maxWidth: '320px',
          height: '39vh',
          fontFamily: 'sans-serif',
          border: '1px solid #e0e7ef',
          background: 'linear-gradient(135deg, #f9fafb 60%, #e0e7ef 100%)',
          boxShadow: 2,
          borderRadius: 3,
          overflow: 'visible',
          overflowX: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          transition: 'box-shadow 0.3s, transform 0.3s',
          cursor: 'pointer',
          '&:hover': {
            boxShadow: 6,
            transform: 'translateY(-4px) scale(1.03)',
            borderColor: '#2563eb',
            background: 'linear-gradient(135deg, #f1f5fe 60%, #dbeafe 100%)',
          }
        }}
      >
        <CardContent
          sx={{
            padding: '14px !important',
            display: 'flex',
            flexDirection: 'column',
            wordBreak: 'break-word',
            fontFamily: 'sans-serif',
            '& a': {
              wordBreak: 'break-all',
              color: '#2563eb',
              textDecoration: 'underline',
            }
          }}
        >
          <Typography variant="subtitle1" fontWeight={700} color="primary" gutterBottom>
            {item.title}
          </Typography>
          <Typography variant="caption" display="block" sx={{ marginBottom: 0.5 }}>
            <b>Services:</b> {item.services.join(', ')}
          </Typography>
          <Typography variant="caption" display="block" sx={{ marginBottom: 0.5 }}>
            <b>Source:</b>{' '}
            <a href={item.source_url} target="_blank" rel="noopener noreferrer">
              {item.source_url}
            </a>
          </Typography>
          <Typography variant="caption" display="block" sx={{ marginBottom: 0.5 }}>
            <b>Scraped:</b> {new Date(item.scraped_at).toLocaleString()}
          </Typography>
          {item.raw_title && (
            <Typography variant="caption" display="block" sx={{ marginBottom: 0.5 }}>
              <b>Raw Title:</b> {item.raw_title}
            </Typography>
          )}
          <Typography variant="caption" display="block">
            <b>Status:</b> {item.parsing_status}
          </Typography>
        </CardContent>
      </Card>
    ))}
  </Box>
);

export default ItemList;
