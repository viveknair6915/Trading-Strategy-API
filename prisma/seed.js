const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  await prisma.tickerData.create({
    data: {
      datetime: new Date('2025-03-20T09:30:00'),
      open: 100.50,
      high: 101.00,
      low: 100.00,
      close: 100.75,
      volume: 1500,
    },
  });
  // Add more records as needed
}

main()
  .catch(e => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
